\ProvidesClass{vorlage-design-main}[2024/11/26 Angepasste Klasse für Artikel]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 1. Klassenoptionen und grundlegende Definitionen
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\ProcessOptions\relax
\ExecuteOptions{}
\LoadClass[twoside,11pt]{article}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 2. Frühe Pakete und grundlegende Bedingungen
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage{etoolbox}          % Werkzeuge für LaTeX-Programmierung
\RequirePackage{ifxetex,ifluatex}  % Engine-Erkennung

% XeTeX/LuaTeX Bedingung
\newif\ifxetexorluatex
\ifxetex
  \xetexorluatextrue
\else
  \ifluatex
    \xetexorluatextrue
  \else
    \xetexorluatexfalse
  \fi
\fi

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 3. Schriftart-Setup
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\ifxetexorluatex
  \RequirePackage[no-math]{fontspec}
  %\RequirePackage{unicode-math}
  \RequirePackage{amsmath}
  \RequirePackage{amssymb}
  \RequirePackage{amsfonts}

  % Sans-Serif-Schriftart für Überschriften
  \setsansfont[
    Path = /Users/jan/Library/Fonts/,
    Extension = .ttf,
    UprightFont = SourceSans3-Regular,
    BoldFont = SourceSans3-Bold,
    ItalicFont = SourceSans3-Italic,
    BoldItalicFont = SourceSans3-BoldItalic,
    Scale = 1.0,
    Ligatures = TeX,
    Kerning = On
  ]{SourceSans3}


  % Hauptschriftart
  \setmainfont[
    Path = /Users/jan/Library/Fonts/,
    BoldFont = texgyretermes-bold.otf,
    ItalicFont = texgyretermes-italic.otf,
    BoldItalicFont = texgyretermes-bolditalic.otf,
    Ligatures = TeX,
    Kerning = On,
    WordSpace = 1.05
  ]{texgyretermes-regular.otf}

  % Monospace-Schriftart für Code
  \setmonofont[
    Path = /Users/jan/Library/Fonts/,
    Extension = .ttf,
    UprightFont = SourceCodePro-Regular,
    BoldFont = SourceCodePro-Bold,
    ItalicFont = SourceCodePro-Italic,
    BoldItalicFont = SourceCodePro-BoldItalic,
    Scale = 0.95
  ]{SourceCodePro-Regular}


  % Mathematische Schriftart
  %\setmathfont{texgyretermes-math.otf}[Path = /Users/jan/Library/Fonts/]

  %% Checkbox-Definitionen
  %\newcommand{\checkbox}{$\square$}
  %\newcommand{\checkmark}{$\checkmark$}
  %\else
  %\RequirePackage[T1]{fontenc}
  %\RequirePackage{newtxtext,newtxmath}
  %\RequirePackage{bbding}
  %\newcommand{\checkbox}{\Square}
  %\newcommand{\checkmark}{\CheckedBox}
  %\fi

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 4. Layout-Pakete und Basis-Einstellungen
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage[ngerman]{babel}    % Deutsche Sprachanpassung
\RequirePackage[ngerman]{datetime2}
\RequirePackage{geometry}          % Seitengeometrie
%\RequirePackage{microtype}         % Typographische Verbesserungen
\RequirePackage{fancyhdr}          % Kopf- und Fußzeilen
\RequirePackage{graphicx}          % Grafikunterstützung
\RequirePackage{xcolor}            % Farben
\RequirePackage{listings}          % Code-Darstellung

% Geometrie-Einstellungen
\geometry{
    paperwidth=20.99cm,
    paperheight=29.70cm,
    top=25mm,
    bottom=25mm,
    inner=25mm,
    outer=25mm,
    headsep=0.762cm,
    footskip=0.762cm,
    footnotesep=1.016cm,
    reversemarginpar,
    marginparwidth=1.4605cm,
    marginparsep=0.5em
}

% Microtype-Einstellungen
%\microtypesetup{
%    protrusion=true,
%    expansion=true,
%    tracking=true,
%    spacing=true,
%    factor=1100,
%    stretch=20,
%    shrink=20
%}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 5. Funktionalitäts-Pakete
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage{tikz}              % Zeichnungen
\usetikzlibrary{mindmap,trees}     % TikZ-Erweiterungen
\RequirePackage{lastpage}          % Letzte Seitennummer
\RequirePackage[medium,small,raggedright,noindentafter]{titlesec}  % Überschriften
\RequirePackage[runin]{abstract}   % Zusammenfassung
\RequirePackage{booktabs}          % Schöne Tabellen
\RequirePackage{caption,subcaption} % Beschriftungen
\RequirePackage{flafter}           % Gleitumgebungen
\RequirePackage[norule,multiple]{footmisc}  % Fußnoten
\RequirePackage{multicol,multirow} % Mehrspaltig/Mehrzeilig
\RequirePackage{enumitem}          % Listenformatierung
\RequirePackage[figuresright]{rotating}  % Gedrehte Elemente
\RequirePackage{lineno}            % Zeilennummern
\RequirePackage{url}               % URL-Formatierung
\RequirePackage{eurosym}           % Eurosymbol
\RequirePackage{pdfpages}          % PDF-Einbindung
\RequirePackage{csquotes}          % Anführungszeichen

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 6. Bibliographie-Setup (Springer-Stil angepasst)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage[
    backend=biber,
    style=authoryear,       % Stil für Springer-authordate
    autocite=footnote,      % Automatisches Zitieren in Fußnoten
    dashed=false,           % Kein "---" für wiederholte Autoren
    isbn=false,             % ISBN ausblenden
    language=german         % Deutsche Lokalisierung
]{biblatex}

% Titelanpassung für verschiedene Publikationstypen
\DeclareFieldFormat[article]{title}{#1\isdot}
\DeclareFieldFormat[incollection]{title}{#1\isdot}
\DeclareFieldFormat[inbook]{title}{#1\isdot}
\DeclareFieldFormat[report]{title}{#1\isdot}
\DeclareFieldFormat[inproceedings]{title}{#1\isdot}
\DeclareFieldFormat[inproceedings]{booktitle}{#1\isdot}
\DeclareFieldFormat[thesis]{title}{#1\isdot}
\DeclareFieldFormat[misc]{title}{#1\isdot}
\DeclareFieldFormat{url}{Verfügbar unter <\url{#1}>}

% Spracheinstellungen für deutsche Begriffe
\DefineBibliographyStrings{german}{%
  in = {\ifentrytype{inproceedings}{In:}{In:}}, % Übersetzung von "In"
}

% Anpassungen bei Büchern (z. B. keine Ortsangabe)
\AtEveryBibitem{%
  \ifentrytype{book}{%
    \clearlist{location}  % Verlagsorte entfernen
    \clearfield{pages}    % Seitenzahl entfernen
  }{}
}

% URL-Stil und Layout
\urlstyle{same}
\setlength{\bibhang}{1em}
\renewcommand{\bibfont}{\small} % Schriftgröße der Bibliographie
\setlength{\bibitemsep}{\z@}    % Zeilenabstand in der Bibliographie


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 7. Farben und Code-Stile
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Farbdefinitionen
\definecolor{red3}{rgb}{0.80, 0.0, 0.0} % Für Warnungen oder kritische Hinweise
\definecolor{blue3}{rgb}{0.0, 0.0, 0.80} % Für Keywords oder wichtige Begriffe
\definecolor{DodgerBlue4}{rgb}{0.06, 0.31, 0.55} % Für Links und Referenzen
\definecolor{DarkOrange}{rgb}{0.85, 0.45, 0.0} % Für Strings oder Hervorhebungen
\definecolor{dunklesgrau}{rgb}{0.1, 0.1, 0.1} % Standardtextfarbe
\definecolor{ForestGreen}{rgb}{0.13, 0.55, 0.13} % Für Kommentare oder Notizen
\definecolor{DarkSlateGray}{rgb}{0.18, 0.31, 0.31} % Für Schlüsselwörter in Code
\definecolor{gray33}{rgb}{0.33, 0.33, 0.33} % Für Sekundärtext oder Randnummern
\definecolor{maroon4}{rgb}{0.55, 0.11, 0.38} % Akzentfarbe für spezielle Elemente
\definecolor{mydarkblue}{HTML}{010625} % Für Überschriften oder starke Kontraste
\definecolor{mydarkred}{HTML}{a30404} % Für kritische Markierungen
\definecolor{webheader}{HTML}{25383C} % Header-Hintergrundfarbe
\definecolor{webrot}{HTML}{B82328} % Akzente oder Warnungen
\definecolor{webgrau}{HTML}{808080} % Neutrale Hinweise oder Hintergrund


% Code-Einstellungen
\lstset{
    basicstyle=\ttfamily\small,
    basewidth={0.5em,0.45em},
    breaklines=true,
    breakatwhitespace=true,
    showspaces=false,
    showstringspaces=false,
    numbers=none, % Zeilennummern deaktiviert
    frame=none, % Rahmen deaktiviert
    tabsize=4,
    captionpos=b,
    keywordstyle=\bfseries\color{DarkSlateGray}, % Für Schlüsselwörter
    commentstyle=\color{ForestGreen}, % Kommentare
    stringstyle=\color{DarkOrange}, % Strings
    keepspaces=true,
    columns=flexible,
    breakindent=2em,
    literate={
        á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1
        {Á}{{\'A}}1 {É}{{\'E}}1 {Í}{{\'I}}1 {Ó}{{\'O}}1 {Ú}{{\'U}}1
        {à}{{\`a}}1 {è}{{\`e}}1 {ì}{{\`i}}1 {ò}{{\`o}}1 {ù}{{\`u}}1
        {À}{{\`A}}1 {È}{{\'E}}1 {Ì}{{\`I}}1 {Ò}{{\`O}}1 {Ù}{{\`U}}1
        {ä}{{\"a}}1 {ë}{{\"e}}1 {ï}{{\"i}}1 {ö}{{\"o}}1 {ü}{{\"u}}1
        {Ä}{{\"A}}1 {Ë}{{\"E}}1 {Ï}{{\"I}}1 {Ö}{{\"O}}1 {Ü}{{\"U}}1
        {â}{{\^a}}1 {ê}{{\^e}}1 {î}{{\^i}}1 {ô}{{\^o}}1 {û}{{\^u}}1
        {Â}{{\^A}}1 {Ê}{{\^E}}1 {Î}{{\^I}}1 {Ô}{{\^O}}1 {Û}{{\^U}}1
        {œ}{{\oe}}1 {Œ}{{\OE}}1 {æ}{{\ae}}1 {Æ}{{\AE}}1 {ß}{{\ss}}1
        {ű}{{\H{u}}}1 {Ű}{{\H{U}}}1 {ő}{{\H{o}}}1 {Ő}{{\H{O}}}1
        {ç}{{\c c}}1 {Ç}{{\c C}}1 {ø}{{\o}}1 {å}{{\r a}}1 {Å}{{\r A}}1
        {€}{{\EUR}}1 {£}{{\pounds}}1 {~}{{\textasciitilde}}1 {-}{{-}}1
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 8. Layout-Konfigurationen
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% --- Basis-Layout ---
\setlength{\headheight}{13.6pt}
\linespread{1.15}
\setlength{\parskip}{0.8em}
\setlength{\parindent}{0pt}

% --- Kopf- und Fußzeilen ---
\fancyhf{}
\renewcommand{\headrulewidth}{1pt}
\fancyhead[RO]{\@runningtitle\quad\textbf{\thepage}}
\fancyhead[LE]{\textbf{\thepage}\quad\@journalname}
\pagestyle{fancy}

\fancypagestyle{firstpage}{%
  \fancyhf{}
  \renewcommand{\headrule}{}
  \fancyfoot[L]{\footnotesize~\\\textcopyright\space\@name, \@jahr}
  \fancyfoot[R]{\footnotesize~\\Seite \thepage\ von \pageref{LastPage}}
}

% --- Titel und Metadaten ---
\newcommand{\runningtitle}[1]{\def\@runningtitle{#1}}
\def\@name{\@author}
\def\@jahr{\the\year}
\def\@journalname{Notizen}

\renewcommand{\@maketitle}{
  \thispagestyle{empty}
  \begin{tikzpicture}[remember picture,overlay]
    \node[anchor=north west, minimum width=\paperwidth, fill=mydarkblue]
      at (current page.north west) {
      \parbox{\textwidth}{
        \vspace*{5pt}
        {\color{webgrau}\LARGE\bfseries\@title\par}
        \vspace{1em}
        {\color{webrot}\Large\@date\par}
        \vspace{5pt}
      }
    };
  \end{tikzpicture}
  \vspace{3cm}
}

\renewcommand{\maketitle}{%
  \vspace*{\dimexpr-\headsep-\baselineskip}%
  \@maketitle\thispagestyle{firstpage}%
}

% --- Abstract-Formatierung ---
\setlength{\abstitleskip}{-\parindent}
\abslabeldelim{\quad}
\setlength{\absleftindent}{1em}
\setlength{\absrightindent}{1em}
\preto{\abstract}{%
  {\noindent\rule{\textwidth}{1pt}}\vspace*{1em}%
}
\appto{\endabstract}{%
  \vspace*{1em}%
  {\noindent\raisebox{1em}{\rule{\textwidth}{1pt}}}\vspace*{\baselineskip}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 9. Formatierungseinstellungen
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% --- Listen-Einstellungen ---
\setlist{
    leftmargin=*,
    align=left,
    widest=00,
    itemsep=0.1em,   % Noch kleinerer Abstand zwischen den Elementen
    parsep=0.1em     % Noch kleinerer Abstand nach Absätzen
}

% --- Caption-Einstellungen ---
\captionsetup*{
    labelfont={bf,footnotesize},
    textfont={it},
    labelsep={period},
    justification=centering,
    singlelinecheck=false
}
\captionsetup*[figure]{name=ABB.}
\captionsetup*[table]{
    name=TAB.,
    position=top,
    justification=raggedright
}

% --- Tabellen-Einstellungen ---
\renewcommand{\arraystretch}{1.15}  % Mehr Platz in Tabellen
\DeclareRobustCommand{\patchINOtable}[1]{%
  \BeforeBeginEnvironment{#1}{\footnotesize}
}
\renewcommand{\belowrulesep}{1em}
\renewcommand{\aboverulesep}{1em}
\setlength{\heavyrulewidth}{1pt}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 10. Überschriften-Formatierung
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% --- Nummerierungstiefe ---
\setcounter{secnumdepth}{0}

% --- Überschriften Format ---
\titleformat{\section}
    {\sffamily\Large\bfseries}     % Format des Titels
    {\thesection}                  % Format der Nummerierung
    {1em}                          % Abstand zwischen Nummer und Titel
    {}                             % Zusätzliche Formatierung
    [\vspace{0.5em}]              % Nach der Überschrift

\titleformat{\subsection}
    {\sffamily\large\bfseries}     % Etwas kleiner als section
    {\thesubsection}
    {1em}
    {}
    [\vspace{0.3em}]

\titleformat{\subsubsection}
    {\sffamily\normalsize\bfseries} % Normale Größe
    {\thesubsubsection}
    {1em}
    {}
    [\vspace{0.2em}]

\titleformat{\paragraph}
    {\sffamily\normalsize\bfseries} % Wie subsubsection, aber ohne Extra-Abstand
    {\theparagraph}
    {1em}
    {}
    []

\titleformat{\subparagraph}
    {\sffamily\normalsize\itshape}  % Kursiv zur Unterscheidung
    {\thesubparagraph}
    {1em}
    {}
    []

% --- Überschriften Abstände ---
\titlespacing{name=\section}
    {0pt}               % Linker Einzug
    {2\baselineskip}    % Abstand zum vorherigen Text
    {\baselineskip}     % Abstand zum nachfolgenden Text

\titlespacing{name=\section,numberless}
    {0pt}               % Linker Einzug
    {2\baselineskip}    % Abstand zum vorherigen Text
    {0.5em}             % Abstand zum nachfolgenden Text

\titlespacing{\subsection}
    {0pt}
    {1.5\baselineskip}
    {0.5\baselineskip}

\titlespacing{\subsubsection}
    {0pt}
    {\baselineskip}
    {0.5\baselineskip}

\titlespacing{\paragraph}
    {0pt}
    {\baselineskip}
    {0.5em}

\titlespacing{\subparagraph}
    {0pt}
    {\baselineskip}
    {0.5em}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 11. Tabellenformatierung
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\AtBeginDocument{%
  \patchINOtable{tabular}
  \patchINOtable{tabular*}
  \patchINOtable{sidewaystable}
  \patchINOtable{sidewaystable*}
  \@ifpackageloaded{tabularx}{\patchINOtable{tabularx}}{}
  \@ifpackageloaded{supertabular}{\patchINOtable{supertabular}}{}
  \@ifpackageloaded{longtable}{
    \patchINOtable{longtable}
    \setlength{\LTleft}{\z@}
  }{}
  \ifdefvoid{\@runningtitle}{\edef\@runningtitle{\@title}}{}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 12. Finale Einstellungen
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% --- Textsatz-Optimierungen ---
\tolerance=2000
\emergencystretch=\maxdimen
\hyphenpenalty=10000
\hbadness=10000

% --- Finale Pakete ---
\AtEndPreamble{
  \RequirePackage[hyperfootnotes=false]{hyperref}
}

\endinput
