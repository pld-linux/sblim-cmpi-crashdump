Summary:	SBLIM CMPI Crash Dump event infrastruktura
Summary(pl.UTF-8):	Infrastruktura obsługi zdarzenia zrzutu awaryjnego dla SBLIM CMPI
Name:		sblim-cmpi-crashdump
Version:	2.0.0
Release:	1
License:	Eclipse Public License v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
# Source0-md5:	2f2a85a563fbb288ddeb7f5255de8606
URL:		http://sblim.sourceforge.net/
BuildRequires:	sblim-cmpi-base-devel
BuildRequires:	sblim-cmpi-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	sblim-cmpi-base
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SBLIM CMPI Crash and Crash Dump Capture Event providers.

%description -l pl.UTF-8
Dostawcy informacji o zdarzeniach awarii i przechwytywania zrzutu
awaryjnego dla SBLIM CMPI.

%prep
%setup -q

%build
%configure \
	CIMSERVER=sfcb \
	PROVIDERDIR=%{_libdir}/cmpi \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_datadir}/%{name}/provider-register.sh \
	-r %{_datadir}/%{name}/Linux_OSCrashDump.registration \
	-m %{_datadir}/%{name}/Linux_OSCrashDump.mof >/dev/null

%preun
if [ "$1" = "0" ]; then
	%{_datadir}/%{name}/provider-register.sh -d \
		-r %{_datadir}/%{name}/Linux_OSCrashDump.registration \
		-m %{_datadir}/%{name}/Linux_OSCrashDump.mof >/dev/null
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/cmpi/libcmpiLinux_OSCrashProvider.so
%dir %{_datadir}/sblim-cmpi-crashdump
%{_datadir}/sblim-cmpi-crashdump/Linux_OSCrashDump.mof
%{_datadir}/sblim-cmpi-crashdump/Linux_OSCrashDump.registration
%attr(755,root,root) %{_datadir}/sblim-cmpi-crashdump/provider-register.sh
