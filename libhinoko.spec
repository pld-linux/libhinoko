#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	GObject introspection library for isochronous communication with devices connected to IEEE 1394 bus
Summary(pl.UTF-8):	Biblioteka GObject introspection do komunikacji izochronicznej z urządzeniami podłączonymi do szyny IEEE 1394
Name:		libhinoko
Version:	1.0.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/alsa-project/libhinoko/tags
Source0:	https://www.kernel.org/pub/linux/libs/ieee1394/%{name}-%{version}.tar.xz
# Source0-md5:	b9f3406fadaa9feb271d5fc9ad980ddd
URL:		https://alsa-project.github.io/gobject-introspection-docs/hinoko/
BuildRequires:	glib2-devel >= 1:2.44.0
BuildRequires:	gobject-introspection-devel >= 1.32.1
%{?with_apidocs:BuildRequires:	gi-docgen >= 2023.1}
BuildRequires:	libhinawa-devel >= 4.0.0
BuildRequires:	meson >= 0.58.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3-pygobject3-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.44.0
Requires:	libhinawa >= 4.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hinoko is an GObject introspection library to transfer/receive
isochronous packets on IEEE 1394 bus.

%description -l pl.UTF-8
Hinoko to biblioteka GObject introspection do przesyłania/odbierania
pakietów izochronicznych poprzez szynę IEEE 1394.

%package devel
Summary:	Header files for hinoko library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki hinoko
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44.0
Requires:	libhinawa-devel >= 4.0.0

%description devel
Header files for hinoko library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki hinoko.

%package static
Summary:	Static hinoko library
Summary(pl.UTF-8):	Statyczna biblioteka hinoko
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static hinoko library.

%description static -l pl.UTF-8
Statyczna biblioteka hinoko.

%package apidocs
Summary:	API documentation for hinoko library
Summary(pl.UTF-8):	Dokumentacja API biblioteki hinoko
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for hinoko library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki hinoko.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Ddoc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/hinoko $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_libdir}/libhinoko.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhinoko.so.1
%{_libdir}/girepository-1.0/Hinoko-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhinoko.so
%{_includedir}/hinoko
%{_datadir}/gir-1.0/Hinoko-1.0.gir
%{_pkgconfigdir}/hinoko.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libhinoko.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/hinoko
%endif
