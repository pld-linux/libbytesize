#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module

Summary:	A library for working with sizes in bytes
Summary(pl.UTF-8):	Biblioteka do pracy z rozmiarami w bajtach
Name:		libbytesize
Version:	2.0
Release:	1
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://github.com/storaged-project/libbytesize/releases
Source0:	https://github.com/storaged-project/libbytesize/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d47369556cd92aad4d8bc8ba10aebbed
Patch0:		%{name}-python2.patch
URL:		https://github.com/storaged-project/libbytesize
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	gmp-devel
BuildRequires:	gtk-doc
BuildRequires:	libtool >= 2:2
BuildRequires:	mpfr-devel
BuildRequires:	pcre2-8-devel
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-devel >= 2}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libbytesize is a C library that facilitates work with sizes in
bytes. Be it parsing the input from users or producing a nice human
readable representation of a size in bytes this library takes
localization into account. It also provides support for sizes bigger
than MAXUINT64.

%description -l pl.UTF-8
libbytesize to biblioteka C ułatwiająca pracę z rozmiarami w bajtach -
np. analizy wejścia od użytkowników czy tworzenia ładnej, czytelnej
dla człowieka reprezentacji rozmiaru w bajtach z uwzględnieniem
lokalizacji. Zapewnia także obsługę rozmiarów większych niż MAXUINT64.

%package devel
Summary:	Header files for libbytesize library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbytesize
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gmp-devel
Requires:	mpfr-devel

%description devel
Header files for libbytesize library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbytesize.

%package apidocs
Summary:	libbytesize library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libbytesize
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for libbytesize library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libbytesize.

%package -n python-bytesize
Summary:	Python 2 bindings for libbytesize
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki libbytesize.
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-six

%description -n python-bytesize
This package contains Python 2 bindings for libbytesize.

%description -n python-bytesize -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona 2 do libbytesize.

%package -n python3-bytesize
Summary:	Python 3 bindings for libbytesize
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libbytesize.
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-six

%description -n python3-bytesize
This package contains Python 3 bindings for libbytesize.

%description -n python3-bytesize -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona 3 do libbytesize.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{!?with_python2:--without-python2} \
	%{!?with_python3:--without-python3}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_gtkdocdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python2}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%if %{with python3}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# no configure option to specify location
%{__mv} $RPM_BUILD_ROOT{%{_datadir}/gtk-doc/html/libbytesize,%{_gtkdocdir}}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libbytesize.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbytesize.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbytesize.so
%{_includedir}/bytesize
%{_pkgconfigdir}/bytesize.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbytesize

%if %{with python2}
%files -n python-bytesize
%defattr(644,root,root,755)
%dir %{py_sitedir}/bytesize
%{py_sitedir}/bytesize/*.py[co]
%endif

%if %{with python3}
%files -n python3-bytesize
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bscalc
%dir %{py3_sitedir}/bytesize
%{py3_sitedir}/bytesize/__pycache__
%{py3_sitedir}/bytesize/*.py
%{_mandir}/man1/bscalc.1*
%endif
