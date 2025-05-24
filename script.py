from rdflib import Graph, Namespace, RDF, OWL

# Função para adicionar tipos de propriedades
def declarar_propriedades(grafo, namespace):
    propriedades = [
        (namespace.estudaCom, [OWL.ObjectProperty, OWL.SymmetricProperty]),
        (namespace.daBasesPara, [OWL.ObjectProperty])
    ]
    for prop, tipos in propriedades:
        for tipo in tipos:
            grafo.add((prop, RDF.type, tipo))

# Função para aplicar CONSTRUCT queries
def aplicar_constructs(grafo, queries):
    for query in queries:
        resultados = grafo.query(query)
        for triplo in resultados:
            grafo.add(triplo)

# Carregar ontologia
grafo = Graph()
grafo.parse("sapientia_ind.ttl", format="turtle")

# Definir namespace
SAP = Namespace("http://www.semanticweb.org/rpcw.di.uminho.pt/2025/2025/sapientia#")

# Declarar propriedades OWL
declarar_propriedades(grafo, SAP)

# Queries CONSTRUCT
queries_construct = [
    """
    PREFIX : <http://www.semanticweb.org/rpcw.di.uminho.pt/2025/2025/sapientia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    CONSTRUCT {
      ?aprendiz :estudaCom ?mestre .
    }
    WHERE {
      ?aprendiz a :Aprendiz ;
                :aprende ?disciplina .
      ?mestre a :Mestre ;
              :ensina ?disciplina .
    }
    """,
    """
    PREFIX : <http://www.semanticweb.org/rpcw.di.uminho.pt/2025/2025/sapientia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    CONSTRUCT {
      ?disciplina :daBasesPara ?aplicacao .
    }
    WHERE {
      ?conceito :éEstudadoEm ?disciplina ;
                :temAplicaçãoEm ?aplicacao .
    }
    """
]

# Aplicar as CONSTRUCTs ao grafo
aplicar_constructs(grafo, queries_construct)

# Serializar grafo final
grafo.serialize(destination="sapientia_final.ttl", format="turtle")
