
import pandas as pd
from pathlib import Path
import torch
from chai_lab.chai1 import run_inference
import shutil
import sys

def main(gpu_index):
    num_gpus = 10

    df = pd.read_csv('gene_alignments3.csv')
    output_cifs_dir = Path("output_cifs")
    
    # Filter out rows where the .cif file already exists
    df = df[~df['ensembl_id'].apply(lambda ensembl_id: (output_cifs_dir / f"{ensembl_id}.cif").exists())]
    total_rows = len(df)
    portion_size = total_rows // num_gpus
    
    start_idx = gpu_index * portion_size
    end_idx = (gpu_index + 1) * portion_size if gpu_index < (num_gpus - 1) else total_rows
    df_gpu = df.iloc[start_idx:end_idx]

    for index, row in df_gpu.iterrows():
        ensembl_id = row['ensembl_id']
        target_rna = row['target_rna']
        
        cif_file = Path(f"output_cifs/{ensembl_id}.cif")
        if cif_file.exists():
            print(f"Skipping {ensembl_id}, output file already exists: {cif_file}")
            continue
        
        print(f"Processing ensembl_id: {ensembl_id}, target_rna: {target_rna}")

        example_fasta = f""">protein|PIK3CB
MYSGAGPALAPPAPPPPIQGYAFKPPPRPDFGTSGRTIKLQANFFEMDIPKIDIYHYELDIKPEKCPRRVNREIVEHMVQHFKTQIFGDRKPVFDGRKNLYTAMPLPIGRDKVELEVTLPGEGKDRIFKVSIKWVSCVSLQALHDALSGRLPSVPFETIQALDVVMRHLPSMRYTPVGRSFFTASEGCSNPLGGGREVWFGFHQSVRPSLWKMMLNIDVSATAFYKAQPVIEFVCEVLDFKSIEEQQKPLTDSQRVKFTKEIKGLKVEITHCGQMKRKYRVCNVTRRPASHQTFPLQQESGQTVECTVAQYFKDRHKLVLRYPHLPCLQVGQEQKHTYLPLEVCNIVAGQRCIKKLTDNQTSTMIRATARSAPDRQEEISKLMRSADFNTDPYVREFGIMVKDEMTDVTGRVLQPPSILYGGRNKAIATPVQGVWDMRNKQFHTGIEIKVWAIACFAPQRQCTEVHLKSFTEQLRKISRDAGMPIQGQPCFCKYAQGADSVEPMFRHLKNTYAGLQLVVVILPGKTPVYAEVKRVGDTVLGMATQCVQMKNVQRTTPQTLSNLCLKINVKLGGVNNILLPQGRPPVFQQPVIFLGADVTHPPAGDGKKPSIAAVVGSMDAHPNRYCATVRVQQHRQEIIQDLAAMVRELLIQFYKSTRFKPTRIIFYRAGVSEGQFQQVLHHELLAIREACIKLEKDYQPGITFIVVQKRHHTRLFCTDKNERVGKSGNIPAGTTVDTKITHPTEFDFYLCSHAGIQGTSRPSHYHVLWDDNRFSSDELQILTYQLCHTYVRCTRSVSIPAPAYYAHLVAFRARYHLVDKEHDAAEGDHTDGQANGRDHQALAKAVQVHQDTLRTMYFA
>rna|AUAGGAUUCAUAUUAGGAGAU
AUAGGAUUCAUAUUAGGAGAU
>rna|PIK3CB_AUAGGAUUCAUAUUAGGAGAU_{ensembl_id}_{target_rna}
{target_rna}"""

        fasta_path = Path(f"fasta/{gpu_index}.fasta")
        fasta_path.write_text(example_fasta)
        print(f"FASTA file written to {fasta_path}")

        output_dir = Path(f"outputdirs/output{gpu_index}")
        output_cif_paths = run_inference(
            fasta_file=fasta_path,
            output_dir=output_dir,
            num_trunk_recycles=3,
            num_diffn_timesteps=200,
            seed=42,
            device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
            use_esm_embeddings=True,
        )

        cif_file = output_dir / "pred.model_idx_0.cif"
        if cif_file.exists():
            new_cif_name = output_cifs_dir / f"{ensembl_id}.cif"
            shutil.move(str(cif_file), str(new_cif_name))
            print(f"Moved {cif_file} to {new_cif_name}")
        else:
            print(f"File {cif_file} does not exist")

if __name__ == "__main__":
    gpu_index = int(sys.argv[1]) 
    main(gpu_index)