#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dieses Modul erstellt eine strukturierte Übersicht zur Verdichtungsänderung in Motoren.

Es visualisiert mittels Graphviz verschiedene Aspekte wie Verdichtung, geometrische Größen,
Bearbeitungsmethoden und weitere relevante Komponenten in einer SVG-Darstellung.
"""

from typing import List

from graphviz import Digraph


def create_overview() -> Digraph:
    """
    Erstellt eine strukturierte Übersicht als Digraph-Objekt.

    Returns:
        Digraph: Ein konfiguriertes Graphviz-Digraph-Objekt mit der kompletten Übersicht.
    """
    overview = Digraph(format="svg", graph_attr={"rankdir": "LR", "bgcolor": "white"})
    overview.attr("node", shape="ellipse", style="filled", fillcolor="lightgrey")
    return overview


def add_main_nodes(overview: Digraph) -> None:
    """
    Fügt die Hauptknoten zum Graphen hinzu.

    Args:
        overview: Das Digraph-Objekt, zu dem die Knoten hinzugefügt werden sollen.
    """
    overview.node("root", "Verdichtungsänderung", fillcolor="lightblue")

    # Erste Ebene: Grundbegriffe
    first_level_nodes = [
        ("verdichtung", "Verdichtung"),
        ("geometrie", "Geometrische Größen"),
        ("bearbeitung", "Bearbeitungsmethoden"),
        ("komponenten", "Motorkomponenten"),
        ("berechnung", "Berechnungsgrößen"),
        ("prozess", "Prozessgrößen"),
    ]

    for node_id, label in first_level_nodes:
        overview.node(node_id, label, fillcolor="lightyellow")
        overview.edge("root", node_id)


def add_detail_nodes(overview: Digraph) -> None:
    """
    Fügt die detaillierten Unterknoten zum Graphen hinzu.

    Args:
        overview: Das Digraph-Objekt, zu dem die Detailknoten hinzugefügt werden sollen.
    """

    def add_nodes_and_edges(
        parent: str, nodes: List[tuple[str, str]], edges: List[tuple[str, str]]
    ) -> None:
        """
        Hilfsfunktion zum Hinzufügen von Knoten und deren Verbindungen.

        Args:
            parent: ID des Elternknotens
            nodes: Liste von Tupeln (node_id, label)
            edges: Liste von Tupeln (from_id, to_id) für die Verbindungen
        """
        for node_id, label in nodes:
            overview.node(node_id, label, fillcolor="white")
        overview.edges(edges)

    # Verdichtung
    verdichtung_nodes = [
        ("verh", "Verdichtungsverhältnis (ε)"),
        ("def_verh", "Definition: Verhältnis des max. zum min. Zylindervolumen"),
        ("bede_verh", "Bedeutung: Bestimmt Wirkungsgrad des Motors"),
        ("einfl_verh", "Einfluss: Brennraumgestaltung, Kolbenform, Geometrie"),
    ]
    verdichtung_edges = [
        ("verdichtung", "verh"),
        ("verh", "def_verh"),
        ("verh", "bede_verh"),
        ("verh", "einfl_verh"),
    ]
    add_nodes_and_edges("verdichtung", verdichtung_nodes, verdichtung_edges)

    # Geometrische Größen
    geometrie_nodes = [
        ("hub", "Hub (s)"),
        ("def_hub", "Definition: Weg zwischen Totpunkten des Kolbens"),
        ("bede_hub", "Bedeutung: Bestimmt Hubraum, Motorcharakteristik"),
        ("bohrung", "Bohrung (d)"),
        ("def_bohrung", "Definition: Innendurchmesser des Zylinders"),
        ("bede_bohrung", "Bedeutung: Bestimmt Kolbenfläche"),
    ]
    geometrie_edges = [
        ("geometrie", "hub"),
        ("hub", "def_hub"),
        ("hub", "bede_hub"),
        ("geometrie", "bohrung"),
        ("bohrung", "def_bohrung"),
        ("bohrung", "bede_bohrung"),
    ]
    add_nodes_and_edges("geometrie", geometrie_nodes, geometrie_edges)

    # Bearbeitungsmethoden
    bearbeitung_nodes = [
        ("abschleifen", "Abschleifen"),
        ("zweck_abs", "Zweck: Präzise Oberflächenbearbeitung"),
        ("anw_abs", "Anwendung: Zylinderkopf, Zylinderblock"),
        ("aufbohren", "Aufbohren"),
        ("zweck_auf", "Zweck: Vergrößerung des Zylinderdurchmessers"),
        ("anw_auf", "Anwendung: Leistungssteigerung"),
    ]
    bearbeitung_edges = [
        ("bearbeitung", "abschleifen"),
        ("abschleifen", "zweck_abs"),
        ("abschleifen", "anw_abs"),
        ("bearbeitung", "aufbohren"),
        ("aufbohren", "zweck_auf"),
        ("aufbohren", "anw_auf"),
    ]
    add_nodes_and_edges("bearbeitung", bearbeitung_nodes, bearbeitung_edges)

    # Motorkomponenten
    komponenten_nodes = [
        ("dichtung", "Zylinderkopfdichtung"),
        ("fkt_dicht", "Funktion: Abdichtung zwischen Kopf und Block"),
        ("bede_dicht", "Bedeutung: Werkzeug zur Verdichtungsanpassung"),
    ]
    komponenten_edges = [
        ("komponenten", "dichtung"),
        ("dichtung", "fkt_dicht"),
        ("dichtung", "bede_dicht"),
    ]
    add_nodes_and_edges("komponenten", komponenten_nodes, komponenten_edges)

    # Berechnungsgrößen
    berechnung_nodes = [
        ("querschnitt", "Zylinderquerschnitt (A)"),
        ("def_quer", "Definition: Kreisfläche des Zylinders"),
        ("berechnung_formel", "Berechnung: A = π * d^2 / 4"),
    ]
    berechnung_edges = [
        ("berechnung", "querschnitt"),
        ("querschnitt", "def_quer"),
        ("querschnitt", "berechnung_formel"),
    ]
    add_nodes_and_edges("berechnung", berechnung_nodes, berechnung_edges)

    # Prozessgrößen
    prozess_nodes = [
        ("druck", "Mittlerer Arbeitsdruck"),
        ("def_druck", "Definition: Durchschnittlicher Druck im Arbeitstakt"),
        ("bede_druck", "Bedeutung: Maß für spezifische Motorleistung"),
    ]
    prozess_edges = [("prozess", "druck"), ("druck", "def_druck"), ("druck", "bede_druck")]
    add_nodes_and_edges("prozess", prozess_nodes, prozess_edges)


def create_and_save_graph(file_path: str) -> str:
    """
    Erstellt und speichert den kompletten Graphen.

    Args:
        file_path: Der Dateipfad, unter dem der Graph gespeichert werden soll.

    Returns:
        str: Der Pfad zur erstellten SVG-Datei.
    """
    overview = create_overview()
    add_main_nodes(overview)
    add_detail_nodes(overview)

    # Rendern der SVG-Datei
    overview.render(file_path, format="svg", cleanup=True)
    return file_path


if __name__ == "__main__":
    output_path = "Verdichtungsänderung"
    result_path = create_and_save_graph(output_path)
    print(f"Graph wurde erfolgreich unter {result_path} gespeichert.")
