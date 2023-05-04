from dbterd.adapters.algos import test_relationship


def run(manifest, catalog, **kwargs):
    """Parse dbt artifacts and export PlantUML file

    Args:
        manifest (dict): Manifest json
        catalog (dict): Catalog json

    Returns:
        Tuple(str, str): File name and the PlantUML content
    """
    return ("output.plantuml", parse(manifest, catalog, **kwargs))


def parse(manifest, catalog, **kwargs):
    """Get the PlantUML content from dbt artifacts

    Args:
        manifest (dict): Manifest json
        catalog (dict): Catalog json

    Returns:
        str: PlantUML content
    """
    tables, relationships = test_relationship.parse(
        manifest=manifest, catalog=catalog, **kwargs
    )

    # Build PlantUML content
    # https://plantuml.com/ie-diagram, https://www.plantuml.com/plantuml/uml
    plantuml = "@startuml\n"
    for table in tables:
        plantuml += 'entity "{table}" {{\n{columns}\n  }}\n'.format(
            table=table.name,
            columns="\n".join([f"    {x.name} : {x.data_type}" for x in table.columns]),
        )

    for rel in relationships:
        key_from = f'"{rel.table_map[1]}"'
        key_to = f'"{rel.table_map[0]}"'
        # NOTE: plant uml doesn't have columns defined in the connector
        new_rel = f"  {key_from} }}|..|| {key_to}\n"
        if new_rel not in plantuml:
            plantuml += new_rel

    plantuml += "@enduml"

    return plantuml
