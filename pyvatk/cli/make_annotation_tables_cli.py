import click

from pyvatk.constants import DATA_PATH, CONTEXT_SETTINGS
from pyvatk.utils.make_tables import (update_interactome_tb,
                                      update_rnaseq_tb,
                                      update_clinvar_tb,
                                      update_gevir_tb,
                                      update_scell_deg_tb,
                                      update_hca_tb,
                                      update_gene_ensembl_ann_tb,
                                      update_gnomad_constraint_metrics_tb)

"""
Generate annotation tables from multiple (raw) sources

"""

output_dir_default = f'{DATA_PATH}/data/ht'


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """A package for gene and variant annotation."""
    pass


def make_annotation_tables_from_raw_sources(ccr: bool = False,
                                            interactome: bool = False,
                                            temporal_rnaseq: bool = False,
                                            clinvar: bool = False,
                                            gevir: bool = False,
                                            scell_heart_deg: bool = False,
                                            hca_rnaseq: bool = False,
                                            gene_ensembl: bool = False,
                                            gnomad_metrics: bool = False,
                                            output_dir: str = output_dir_default,
                                            default_ref_genome: str = 'GRCh38'):
    if interactome:
        bed_ppi = update_interactome_tb()
        bed_ppi.checkpoint(
            f'{output_dir}/interactome.{default_ref_genome}.ht',
            overwrite=True
        )

    if temporal_rnaseq:
        rnaseq_tb = update_rnaseq_tb()
        rnaseq_tb.checkpoint(
            f'{output_dir}/rnaseq.human.ht',
            overwrite=True
        )

    if clinvar:
        clinvar_tb = update_clinvar_tb()
        clinvar_tb.checkpoint(
            f'{output_dir}/clinvar.{default_ref_genome}.ht',
            overwrite=True
        )

    if gevir:
        gevir_tb = update_gevir_tb()
        gevir_tb.checkpoint(
            f'{output_dir}/gevir.metrics.ht',
            overwrite=True
        )

    if scell_heart_deg:
        deg_tb = update_scell_deg_tb()
        deg_tb.checkpoint(
            f'{output_dir}/scell.heart.degs.ht',
            overwrite=True
        )

    if hca_rnaseq:
        hca_tb = update_hca_tb()
        hca_tb.checkpoint(
            f'{output_dir}/hca.heart.ht',
            overwrite=True
        )

    if gene_ensembl:
        gene_tb = update_gene_ensembl_ann_tb()
        gene_tb.checkpoint(
            f'{output_dir}/gene.ann.ensembl.ht',
            overwrite=True
        )

    if gnomad_metrics:
        gnomad_tb = update_gnomad_constraint_metrics_tb()
        gnomad_tb.checkpoint(
            f'{output_dir}/gnomad.metrics.ht',
            overwrite=True
        )


@click.command('mktables', short_help='Create annotation tables from raw sources.')
@click.option('--ccr',
              is_flag=True, help='Create/update CCR table from source.')
@click.option('--interactome',
              is_flag=True, help='Create/update CCR table from source.')
@click.option('--temporal_rnaseq',
              is_flag=True, help='Create/update RNAseq table from source.')
@click.option('--clinvar',
              is_flag=True, help='Create/update Clinvar table from source.')
@click.option('--gevir',
              is_flag=True, help='Create/update GeVIR score table from raw source.')
@click.option('--scell_heart_deg',
              is_flag=True, help='Create/update table with DEGs from cardiac-specific cell clusters')
@click.option('--hca_rnaseq',
              is_flag=True, help='Create/update table with gene/cell expression levels from HCA dataset (UCSC)')
@click.option('--gene_ensembl',
              is_flag=True, help='Create/update gene annotation table from Ensembl.')
@click.option('--gnomad_metrics',
              is_flag=True, help='Create/update transcript-specific constraint metrics from gnomad database')
@click.option('--output_dir',
              default=output_dir_default, type=str, help='Output directory to copy created Hail tables')
@click.option('--default_ref_genome',
              default='GRCh38', type=str, help='Default reference genome to start Hail')
@click.pass_context
def make_annotation_tables_cli(ctx, ccr, interactome, temporal_rnaseq, clinvar, gevir, scell_heart_deg, hca_rnaseq,
                               gene_ensembl, gnomad_metrics, output_dir, default_ref_genome):
    make_annotation_tables_from_raw_sources(ccr,
                                            interactome,
                                            temporal_rnaseq,
                                            clinvar,
                                            gevir,
                                            scell_heart_deg,
                                            hca_rnaseq,
                                            gene_ensembl,
                                            gnomad_metrics,
                                            output_dir,
                                            default_ref_genome)


if __name__ == '__main__':
    cli()