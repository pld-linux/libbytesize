Summary:	A library for working with sizes in bytes
Name:		libbytesize
Version:	1.2
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://github.com/storaged-project/libbytesize/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	874d37f534aa9e265013434ef7ab0342
URL:		https://github.com/storaged-project/libbytesize
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gmp-devel
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	mpfr-devel
BuildRequires:	pcre-devel >= 8.32
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libbytesize is a C library that facilitates work with sizes in
bytes. Be it parsing the input from users or producing a nice human
readable representation of a size in bytes this library takes
localization into account. It also provides support for sizes bigger
than MAXUINT64.

%package devel
Summary:	Header files for libbytesize library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbytesize
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-six

%description -n python-bytesize
This package contains Python 2 bindings for libbytesize.

%package -n python3-bytesize
Summary:	Python 3 bindings for libbytesize
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-six

%description -n python3-bytesize
This package contains Python 3 bindings for libbytesize.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_gtkdocdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

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

%files -n python-bytesize
%defattr(644,root,root,755)
%dir %{py_sitedir}/bytesize
%{py_sitedir}/bytesize/*.py[co]

%files -n python3-bytesize
%defattr(644,root,root,755)
%dir %{py3_sitedir}/bytesize
%{py3_sitedir}/bytesize/__pycache__
%{py3_sitedir}/bytesize/*.py
