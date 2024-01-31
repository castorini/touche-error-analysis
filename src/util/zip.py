import shutil

output_filename = "tasb-run-webis-touche2020"
dir_name = "/store2/scratch/n3thakur/touche-ablations/output/tas-b/all_annotators"

shutil.make_archive(output_filename, 'zip', dir_name)
