# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}

%define section free

Name:           javacc
Version:        4.1
Release:        0.5%{?dist}
Epoch:          0
Summary:        A parser/scanner generator for java
License:        BSD
Source0:        https://javacc.dev.java.net/files/documents/17/108015/%{name}-%{version}src.tar.gz
Source1:        javacc.sh
Source2:        jjdoc
Source3:        jjtree
#Jar used for bootstrapping
Source4:	javacc.jar
URL:            https://javacc.dev.java.net/
Group:          Development/Code Generators
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:       java, jpackage-utils >= 0:1.5
BuildRequires:  ant, ant-junit, junit >= 0:3.8.1
BuildRequires:  java-devel, jpackage-utils >= 0:1.5

%if %{with_gcj}
BuildRequires:          java-gcj-compat-devel >= 1.0.31
Requires(post):         java-gcj-compat >= 1.0.31
Requires(postun):       java-gcj-compat >= 1.0.31
%else
BuildArch:      noarch
%endif

%description 
Java Compiler Compiler (JavaCC) is the most popular parser generator for use
with Java applications. A parser generator is a tool that reads a grammar
specification and converts it to a Java program that can recognize matches to
the grammar. In addition to the parser generator itself, JavaCC provides other
standard capabilities related to parser generation such as tree building (via
a tool called JJTree included with JavaCC), actions, debugging, etc.

%package manual
Summary:        Manual for %{name}
Group:          Development/Documentation
Requires:       %{name} = %{version}-%{release}

%description manual
Manual for %{name}.

%package demo
Summary:        Examples for %{name}
Group:          Development/Documentation
Requires:       %{name} = %{version}-%{release}

%description demo
Examples for %{name}.

%prep
%setup -q -n %{name}

# Remove binary information in the source tar
find . -name "*.jar" -exec rm {} \;
find . -name "*.class" -exec rm {} \;

cp -p %{SOURCE1} bin/javacc
cp -p %{SOURCE2} bin/jjdoc
cp -p %{SOURCE3} bin/jjtree

cp -p %{SOURCE4} bootstrap/javacc.jar

%build
# Use the bootstrap javacc.jar to generate some required
# source java files. After these source files are generated we
# remove the bootstrap jar and build the binary from source.
ant -f src/org/javacc/parser/build.xml parser-files
ant -f src/org/javacc/jjtree/build.xml tree-files
find . -name "*.jar" -exec rm {} \;
ant jar

%install
rm -fr $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 bin/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -d -m 755 $RPM_BUILD_ROOT/%{_bindir}
install -m 755 bin/javacc bin/jjdoc bin/jjrun bin/jjtree $RPM_BUILD_ROOT/%{_bindir}
install -d -m 755 $RPM_BUILD_ROOT/%{_datadir}/%{name}
cp -pr examples $RPM_BUILD_ROOT/%{_datadir}/%{name}

%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*.jar
%doc LICENSE README
%defattr(0755,root,root,0755)
/usr/bin/*

%if %{with_gcj}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files manual
%defattr(0644,root,root,0755)
%doc www/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}/*

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:4.1-0.5
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 03 2008 Matt Wringe <mwringe@redhat.com> - 0:4.1-0.2
- Update to remove packaged jars in source tar
- Build with bootstrap jar so that required java source 
  files get generated

* Wed Oct 22 2008 Jerry James <loganjerry@gmail.com> - 0:4.1-0.1
- Update to 4.1
- Also ship the jjrun script
- Own the appropriate gcj directory
- Minor spec file changes to comply with latest Fedora guidelines
- Include the top-level index.html file in the manual

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:4.0-4.5
- drop repotag

* Fri Feb 22 2008 Matt Wringe <mwringe at redhat.com> - 0:4.0-4jpp.4
- Rename javacc script file to javacc.sh as this confuses the makefile

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:4.0-4jpp.3
- Autorebuild for GCC 4.3

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> - 0:4.0-3jpp.3
- Rebuilt with new naming convention

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:4.0-3jpp_2fc
- Rebuilt

* Tue Jul 18 2006 Matthew Wringe <mwringe at redhat.com> - 0:4.0-3jpp_1fc
- Merged with upstream version
- Changed directory locations to rpm macros
- Added conditional native compiling

* Thu Apr 20 2006 Fernando Nasser <fnasser@redhat.com> - 0:4.0-2jpp
- First JPP 1.7 build

* Fri Mar 31 2006 Sebastiano Vigna <vigna at acm.org> - 0:4.0-1jpp
- Updated to 4.0

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.2-2jpp
- Rebuild with ant-1.6.2

* Fri Jan 30 2004 Sebastiano Vigna <vigna at acm.org> 0:3.2-1jpp
- First JPackage version
