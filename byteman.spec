# TODO:
# - build from source, see e.g.:
# http://pkgs.fedoraproject.org/cgit/byteman.git/plain/byteman.spec
# - javadocs
#
%include	/usr/lib/rpm/macros.java
Summary:	Java agent-based bytecode injection tool
Summary(pl.UTF-8):	Oparte na agencie narzędzie do wstrzykiwania kodu dla Javy
Name:		byteman
Version:	3.0.1
Release:	1
License:	LGPL v2+
Group:		Development/Languages/Java
#Source0Download: https://www.jboss.org:443/byteman/downloads.html
Source0:	http://downloads.jboss.org/byteman/%{version}/byteman-download-%{version}-full.zip
# Source0-md5:	c704769662f4dd06233dc659f2d24329
URL:		http://www.jboss.com/byteman/
# this is needed for the LC_ALL=en_US in build part dependency
%if %(locale -a | grep -q '^en_US$'; echo $?)
#BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
# to build from source:
#BuildRequires:	jarjar
#BuildRequires:	java_cup
#BuildRequires:	javapackages-tools
#BuildRequires:	jdk
#BuildRequires:	junit4
#BuildRequires:	maven-failsafe-plugin
#BuildRequires:	maven-jar-plugin
#BuildRequires:	maven-local
#BuildRequires:	maven-shade-plugin
#BuildRequires:	maven-surefire-plugin
#BuildRequires:	maven-surefire-provider-junit4
#BuildRequires:	maven-surefire-provider-testng
#BuildRequires:	maven-verifier-plugin
#BuildRequires:	objectweb-asm
#BuildRequires:	testng
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Byteman is a tool which simplifies tracing and testing of Java
programs. Byteman allows you to insert extra Java code into your
application, either as it is loaded during JVM startup or even after
it has already started running. The injected code is allowed to access
any of your data and call any application methods, including where
they are private. You can inject code almost anywhere you want and
there is no need to prepare the original source code in advance nor do
you have to recompile, repackage or redeploy your application. In fact
you can remove injected code and reinstall different code while the
application continues to execute.

%description -l pl.UTF-8
Byteman to narzędzie upraszczajace śledzenie i testowanie programów w
Javie. Pozwala wstawić dodatkowy kod w Javie do aplikacji - albo w
trakcie wczytywania go przy uruchamianiu JVM, albo nawet po jej
uruchomieniu. Wstrzyknięty kod ma dostęp do dowolnych danych i może
wywoływać dowolne metody aplikacji, włącznie z prywatnymi. Kod można
wstrzyknąć prawie wszędzie i nie ma potrzeby wcześniejszego
przygotowywania kodu źródłowego ani rekompilacji, ponownego
pakietowania ani wdrażania aplikacji. W praktyce można usunąć
wstrzyknięty kod i zainstalować inny kod, kiedy aplikacja cały czas
działa.

%package javadoc
Summary:	Javadocs for Byteman
Summary(pl.UTF-8):	Dokumentacja w formacie javadoc do Bytemana
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadocs for Byteman.

%description javadoc -l pl.UTF-8
Dokumentacja w formacie javadoc do Bytemana.

%prep
%setup -q -n byteman-download-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir}/byteman,%{_datadir}/byteman/{bin,lib},%{_bindir}}

cp -p lib/byteman*.jar contrib/bmunit/byteman-bmunit.jar contrib/dtest/byteman-dtest.jar \
	$RPM_BUILD_ROOT%{_javadir}/byteman
for f in $RPM_BUILD_ROOT%{_javadir}/byteman/byteman*.jar ; do
	ln -sf %{_javadir}/$(basename $f) $RPM_BUILD_ROOT%{_datadir}/byteman/lib
done
install bin/{bmcheck,bmjava,bminstall,bmsubmit}.sh $RPM_BUILD_ROOT%{_datadir}/byteman/bin
for f in bmcheck bmjava bminstall bmsubmit ; do
cat >$RPM_BUILD_ROOT%{_bindir}/$f <<EOF
#!/bin/sh

BYTEMAN_HOME=%{_datadir}/byteman
JAVA_HOME=%{_jvmdir}/java

\$BYTEMAN_HOME/bin/${f}.sh "\$@"
EOF
done

# TODO: javadocs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bmcheck
%attr(755,root,root) %{_bindir}/bmjava
%attr(755,root,root) %{_bindir}/bminstall
%attr(755,root,root) %{_bindir}/bmsubmit
%{_javadir}/byteman
%dir %{_datadir}/byteman
%dir %{_datadir}/byteman/bin
%attr(755,root,root) %{_datadir}/byteman/bin/*.sh
%{_datadir}/byteman/lib

# TODO
#%files javadoc
#%defattr(644,root,root,755)
#%{_javadocdir}/byteman-%{version}
