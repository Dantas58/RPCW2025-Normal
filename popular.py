import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF


ns = Namespace("http://www.sapientia.org/ontologia#")

g = Graph()
g.parse("sapientia_base.ttl", format="ttl")
g.bind("", ns, override=True)


def safe_uri(name):
    return URIRef(ns + name.replace(" ", "_"))

def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

conceitos = load_json("conceitos.json")["conceitos"]
disciplinas = load_json("disciplinas.json")["disciplinas"]
mestres = load_json("mestres.json")["mestres"]
obras = load_json("obras.json")["obras"]
aprendizes = load_json("pg57599.json")

# === Povoa conceitos ===
conceito_map = {}
for c in conceitos:
    uri = safe_uri(c["nome"])
    g.add((uri, RDF.type, ns.Conceito))
    g.add((uri, ns.nome, Literal(c["nome"])))
    conceito_map[c["nome"]] = uri

    for app in c.get("aplicações", []):
        app_uri = safe_uri(app)
        g.add((app_uri, RDF.type, ns.Aplicacao))
        g.add((app_uri, ns.nome, Literal(app)))
        g.add((uri, ns.temAplicacaoEm, app_uri))

    if "períodoHistórico" in c:
        periodo_uri = safe_uri(c["períodoHistórico"])
        g.add((periodo_uri, RDF.type, ns.PeriodoHistorico))
        g.add((periodo_uri, ns.nome, Literal(c["períodoHistórico"])))
        g.add((uri, ns.surgeEm, periodo_uri))

    for rel in c.get("conceitosRelacionados", []):
        rel_uri = conceito_map.get(rel)
        if not rel_uri:
            rel_uri = safe_uri(rel)
            g.add((rel_uri, RDF.type, ns.Conceito))
            g.add((rel_uri, ns.nome, Literal(rel)))
            conceito_map[rel] = rel_uri
        g.add((uri, ns.estáRelacionadoCom, rel_uri))

# === Povoa disciplinas ===
for d in disciplinas:
    disc_uri = safe_uri(d["nome"])
    g.add((disc_uri, RDF.type, ns.Disciplina))
    g.add((disc_uri, ns.nome, Literal(d["nome"])))

    for tipo in d.get("tiposDeConhecimento", []):
        tipo_uri = safe_uri(tipo)
        g.add((tipo_uri, RDF.type, ns.TipoDeConhecimento))
        g.add((tipo_uri, ns.nome, Literal(tipo)))
        g.add((disc_uri, ns.pertenceA, tipo_uri))

    for conceito in d.get("conceitos", []):
        conc_uri = conceito_map.get(conceito)
        if not conc_uri:
            conc_uri = safe_uri(conceito)
            g.add((conc_uri, RDF.type, ns.Conceito))
            g.add((conc_uri, ns.nome, Literal(conceito)))
            conceito_map[conceito] = conc_uri
        g.add((disc_uri, ns.estuda, conc_uri))

for m in mestres:
    mestre_uri = safe_uri(m["nome"])
    g.add((mestre_uri, RDF.type, ns.Mestre))
    g.add((mestre_uri, ns.nome, Literal(m["nome"])))

    if "períodoHistórico" in m:
        periodo_uri = safe_uri(m["períodoHistórico"])
        g.add((periodo_uri, RDF.type, ns.PeriodoHistorico))
        g.add((periodo_uri, ns.nome, Literal(m["períodoHistórico"])))
        g.add((mestre_uri, ns.viveuEm, periodo_uri))

    for disc in m.get("disciplinas", []):
        disc_uri = safe_uri(disc)
        g.add((disc_uri, RDF.type, ns.Disciplina))
        g.add((disc_uri, ns.nome, Literal(disc)))
        g.add((mestre_uri, ns.ensina, disc_uri))

for o in obras:
    obra_uri = safe_uri(o["titulo"])
    g.add((obra_uri, RDF.type, ns.Obra))
    g.add((obra_uri, ns.nome, Literal(o["titulo"])))

    autor_uri = safe_uri(o["autor"])
    g.add((autor_uri, RDF.type, ns.Mestre))
    g.add((autor_uri, ns.nome, Literal(o["autor"])))
    g.add((obra_uri, ns.foiEscritoPor, autor_uri))

    for conceito in o.get("conceitos", []):
        conc_uri = conceito_map.get(conceito)
        if not conc_uri:
            conc_uri = safe_uri(conceito)
            g.add((conc_uri, RDF.type, ns.Conceito))
            g.add((conc_uri, ns.nome, Literal(conceito)))
            conceito_map[conceito] = conc_uri
        g.add((obra_uri, ns.explica, conc_uri))


for a in aprendizes:
    apr_uri = safe_uri(a["nome"])
    g.add((apr_uri, RDF.type, ns.Aprendiz))
    g.add((apr_uri, ns.nome, Literal(a["nome"])))
    g.add((apr_uri, ns.idade, Literal(a["idade"])))

    for disc in a.get("disciplinas", []):
        disc_uri = safe_uri(disc)
        g.add((disc_uri, RDF.type, ns.Disciplina))
        g.add((disc_uri, ns.nome, Literal(disc)))
        g.add((apr_uri, ns.aprende, disc_uri))
        


g.serialize(destination="sapientia_ind.ttl", format="ttl")
