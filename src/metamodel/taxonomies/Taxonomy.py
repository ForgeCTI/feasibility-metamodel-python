from __future__ import annotations

from dataclasses import dataclass, field

from metamodel.taxonomies.TaxonomyConcept import TaxonomyConcept


@dataclass
class Taxonomy:
    id: str
    version: str
    source: str | None = None
    concepts: dict[str, TaxonomyConcept] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "Taxonomy":
        meta = data.get("taxonomy", data)
        tax = cls(id=meta["id"], version=str(meta.get("version", "unknown")), source=meta.get("source"))
        for concept_data in meta.get("concepts", []):
            concept = TaxonomyConcept(
                id=concept_data["id"],
                name=concept_data.get("name", concept_data["id"]),
                description=concept_data.get("description"),
                aliases=list(concept_data.get("aliases", [])),
                category=concept_data.get("category"),
                external_references=list(concept_data.get("external_references", [])),
                tags=list(concept_data.get("tags", [])),
                properties=dict(concept_data.get("properties", {})),
            )
            tax.concepts[concept.id] = concept
        return tax

    def get(self, concept_id: str) -> TaxonomyConcept | None:
        if concept_id in self.concepts:
            return self.concepts[concept_id]
        lowered = concept_id.lower()
        for concept in self.concepts.values():
            if concept.name.lower() == lowered or lowered in [alias.lower() for alias in concept.aliases]:
                return concept
        return None
