#!/local/cluster/bin/python2.7
import getopt, sys
#This script will take the output of Kraken (after tallying the taxIDs) and convert it into the CAMI format output

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "h:i:o:s:", ["Help=", "InputFile=", "OutputFile=", "SampleID="])
	except getopt.GetoptError:
		print 'Unknown options, call using: ./KrakenToCAMI.py -i <InputFile.fq> -o <Outputfile.profile> -s <SampleID>'
		sys.exit(2)
	for opt, arg in opts:
		if opt =='-h':
			print 'Call using: ./KrakenToCAMI.py -i <InputFile.fq> -o <Outputfile.profile> -s <SampleID>'
			sys.exit(2)
		elif opt in ("-i", "--InputFile"):
			file = arg
		elif opt in ("-s", "--SampleID"):
			sample_ID = arg
		elif opt in ("-o", "--OutputFile"):
			outfile = arg


	taxa_and_counts = list();
	fid = open(file,"r")
	for line in fid:
		line_stripped = line.strip()
		line_stripped_split = line_stripped.split('\t')
		taxa_and_counts.append(line_stripped_split)

	fid.close()

	total_reads = 0
	for record in taxa_and_counts:
		total_reads = total_reads + int(record[-1])

	fid = open(outfile,"w")
	fid.write("# CAMI Submission for Taxonomic Profiling\n")
	fid.write("@Version:0.9.1\n")
	fid.write("@SampleID:%s\n" % sample_ID)
	fid.write("@Ranks: superkingdom|phylum|class|order|family|genus|species|strain\n")
	fid.write("\n")
	fid.write("@@TAXID\tRANK\tTAXPATH\tTAXPATHSN\tPERCENTAGE\n")

	ranks=["superkingdom","phylum","class","order","family","genus","species","strain"];
	taxa_dict = dict()
	for record in taxa_and_counts:
		taxpath_split = record[2].split("|")
		taxpath_indicies = list();
		iter = 0;
		rank_diff_list = list();
		prev_rank = 0;
		#loop through the taxpath of a record, only record the acceptable ranks
		for taxa_name in taxpath_split:
			taxa_name_split = taxa_name.split("__")
			if taxa_name_split[0] in ranks:
				rank_diff_list.append(ranks.index(taxa_name_split[0])-prev_rank-1)
				prev_rank = ranks.index(taxa_name_split[0])
				taxpath_indicies.append(iter)
				joined_path = ""
				#joined_path = "|".join([taxpath_split[i] for i in taxpath_indicies])
				for i in taxpath_indicies:
					if taxpath_indicies.index(i)>0:
						joined_path = joined_path + "".join(["|___" for dummy in range(rank_diff_list[taxpath_indicies.index(i)])])
						joined_path = joined_path + "|" + taxpath_split[i]
					else:
						joined_path = taxpath_split[i]
				if joined_path in taxa_dict:
					taxa_dict[joined_path] = taxa_dict[joined_path] + int(record[-1])
				else:
					taxa_dict[joined_path] = int(record[-1])
				iter = iter + 1;
			else:
				iter = iter + 1;			


	#print to file
	for length in range(len(ranks)):
		for name in taxa_dict.keys():
			name_split = name.split("|")
			if len(name_split)==length+1:
				fid.write("%s\t%s\t%s\t%s\t%f\n" % (name.split("|")[-1].split("_")[2], name.split("|")[-1].split("_")[0], "|".join([temp.split("_")[2] for temp in name.split("|")]), "|".join(["_".join(temp.split("_")[3:]) for temp in name.split("|")]), 100*float(taxa_dict[name])/float(total_reads)))

	fid.close()

if __name__ == "__main__":
	main(sys.argv[1:])