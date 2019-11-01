Name     : docbook-xml
Version  : 4.5
Release  : 22
URL      : http://www.docbook.org/xml/4.5/docbook-xml-4.5.zip
Source0  : http://www.docbook.org/xml/4.5/docbook-xml-4.5.zip
Source1  : http://www.docbook.org/sgml/4.5/docbook-4.5.zip
Source2  : https://github.com/docbook/xslt10-stylesheets/releases/download/release%2F1.79.2/docbook-xsl-1.79.2.tar.bz2
Source3	 : nodate.patch
Summary  : No detailed summary available
Group    : Development/Tools
License  : MIT
BuildRequires: /usr/bin/xmlcatalog


%define abi_package %{nil}
%define debug_package %{nil}

%description
No detailed description available

%prep
%setup -q -c -n docbook-xml


%build
mkdir -p docbook-sgml
pushd docbook-sgml
unzip %{SOURCE1}
popd
tar xf %{SOURCE2}
cat %{SOURCE3} | patch -p0

%install
rm -rf %{buildroot}
install -v -d -m755 %{buildroot}/usr/share/xml/docbook/xml-dtd-4.5
install -v -d -m755 %{buildroot}/usr/share/defaults/xml
cp -v -af docbook.cat *.dtd ent/ *.mod %{buildroot}/usr/share/xml/docbook/xml-dtd-4.5

pushd docbook-xsl-*
install -v -m755 -d %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.79.2

cp -v -R VERSION common eclipse epub extensions fo highlighting html \
         htmlhelp images javahelp lib manpages params profiling \
         roundtrip slides template tests tools webhelp website \
         xhtml xhtml-1_1 \
    %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.79.2

ln -s VERSION %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.79.2/VERSION.xsl

popd

pushd docbook-sgml
sed -i -e '/ISO 8879/d' -e '/gml/d' docbook.cat
install -v -d %{buildroot}/usr/share/sgml/docbook/sgml-dtd-4.5
install -v docbook.cat %{buildroot}/usr/share/sgml/docbook/sgml-dtd-4.5/catalog
cp -v -af *.dtd *.mod *.dcl %{buildroot}/usr/share/sgml/docbook/sgml-dtd-4.5
cat >> %{buildroot}/usr/share/sgml/docbook/sgml-dtd-4.5/catalog << "EOF"
  -- Begin Single Major Version catalog changes --

PUBLIC "-//OASIS//DTD DocBook V4.4//EN" "docbook.dtd"
PUBLIC "-//OASIS//DTD DocBook V4.3//EN" "docbook.dtd"
PUBLIC "-//OASIS//DTD DocBook V4.2//EN" "docbook.dtd"
PUBLIC "-//OASIS//DTD DocBook V4.1//EN" "docbook.dtd"
PUBLIC "-//OASIS//DTD DocBook V4.0//EN" "docbook.dtd"

  -- End Single Major Version catalog changes --
EOF

mkdir -p %{buildroot}/usr/share/defaults/sgml
echo 'CATALOG "/usr/share/sgml/docbook/sgml-dtd-4.5/catalog"' > %{buildroot}/usr/share/defaults/sgml/catalog

xmlcatalog --noout --create %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --create %{buildroot}/usr/share/defaults/xml/catalog
xmlcatalog --noout --add "public" "-//OASIS//DTD DocBook XML V4.5//EN" "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --add "public" "-//OASIS//DTD DocBook XML CALS Table Model V4.5//EN" "file:///usr/share/xml/docbook/xml-dtd-4.5/calstblx.dtd" %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --add "public" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5/soextblx.dtd" \
    %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Information Pool V4.5//EN" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5/dbpoolx.mod" \
    %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.5//EN" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5/dbhierx.mod" \
    %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML HTML Tables V4.5//EN" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5/htmltblx.mod" \
    %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Notations V4.5//EN" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5/dbnotnx.mod" \
    %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Character Entities V4.5//EN" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5/dbcentx.mod" \
    %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.5//EN" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5/dbgenent.mod" \
    %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/4.5" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5" \
    %{buildroot}/usr/share/defaults/xml/docbook
xmlcatalog --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/4.5" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5" \
    %{buildroot}/usr/share/defaults/xml/docbook

for DTDVERSION in 4.1.2 4.2 4.3 4.4 4.5
do
  xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML V$DTDVERSION//EN" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION/docbookx.dtd" \
    %{buildroot}/usr/share/defaults/xml/docbook
  xmlcatalog --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5" \
    %{buildroot}/usr/share/defaults/xml/docbook
  xmlcatalog --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION" \
    "file:///usr/share/xml/docbook/xml-dtd-4.5" \
    %{buildroot}/usr/share/defaults/xml/docbook
  xmlcatalog --noout --add "delegateSystem" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
    "file:///usr/share/defaults/xml/docbook" \
    %{buildroot}/usr/share/defaults/xml/catalog
  xmlcatalog --noout --add "delegateURI" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
    "file:///usr/share/defaults/xml/docbook" \
    %{buildroot}/usr/share/defaults/xml/catalog
done

xmlcatalog --noout --add "rewriteSystem" \
           "http://docbook.sourceforge.net/release/xsl/1.79.2" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.2" \
    %{buildroot}/usr/share/defaults/xml/catalog

xmlcatalog --noout --add "rewriteURI" \
           "http://docbook.sourceforge.net/release/xsl/1.79.2" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.2" \
    %{buildroot}/usr/share/defaults/xml/catalog

xmlcatalog --noout --add "rewriteSystem" \
           "http://docbook.sourceforge.net/release/xsl/current" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.2" \
    %{buildroot}/usr/share/defaults/xml/catalog

xmlcatalog --noout --add "rewriteURI" \
           "http://docbook.sourceforge.net/release/xsl/current" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.2" \
    %{buildroot}/usr/share/defaults/xml/catalog

xmlcatalog --noout --add "delegatePublic" "-//OASIS//DTD DocBook XML" "file:///usr/share/defaults/xml/docbook" %{buildroot}/usr/share/defaults/xml/catalog

%files
%defattr(-,root,root,-)
/usr/share/defaults/xml/catalog
/usr/share/defaults/xml/docbook
/usr/share/defaults/sgml/catalog
/usr/share/xml/docbook/xml-dtd-4.5/*
/usr/share/xml/docbook/xsl-stylesheets-1.79.2/*
/usr/share/sgml/docbook/sgml-dtd-4.5/*

