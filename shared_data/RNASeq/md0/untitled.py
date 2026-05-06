cmd.align("ENSG00000100811_gna", "ENSG00000100811_unmod")



cmd.select("only_C3_ref", "ENSG00000100811_unmod and (name C3' or name C3G)")
cmd.select("only_C3_comp", "ENSG00000100811_gna and (name C3' or name C3G)")
cmd.select("first_rna_base_comp", "only_C3_comp and resi 1")
cmd.select("first_rna_base_ref", "only_C3_ref and resi 1")
cmd.distance("dist_a_1", "first_rna_base_ref", "first_rna_base_comp")
print(cmd.get("dist_a_1"))



cmd.select("first_rna_base_comp_b", "only_C3_comp and resi 1 and not first_rna_base_comp")
cmd.select("first_rna_base_ref_b", "only_C3_ref and resi 1 and not first_rna_base_ref")
cmd.distance("dist_b_1", "first_rna_base_ref_b", "first_rna_base_comp_b")
print(cmd.get("dist_b_1"))