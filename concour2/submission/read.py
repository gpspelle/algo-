import pstats
p = pstats.Stats('output_file')
p.sort_stats('cumulative').print_stats()
