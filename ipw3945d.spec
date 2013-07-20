Summary:	The regulatory daemon for controlling and configuring ipw3945 cards
Summary(pl.UTF-8):	Demon do kontrolowania i konfigurowania kart ipw3945
Name:		ipw3945d
Version:	1.7.22
Release:	3
License:	Intel Limited patents license
Group:		Daemons
Source0:	http://bughost.org/ipw3945/daemon/%{name}-%{version}.tgz
# Source0-md5:	097888f5be05eb2b9b87dcdbeeb948ce
Source1:	%{name}.init
URL:		http://bughost.org/ipw3945/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The regulatory daemon is responsible for controlling and configuring
aspects of the hardware required to operate the device within
compliance of various regulatory agencies. This includes controlling
which channels are allowed to do active/passive scanning, transmit
power levels, which channels are allowed to be transmitted on, and
support for IEEE 802.11h (DFS and TPC).

%description -l pl.UTF-8
Demon regulujący jest odpowiedzialny za kontrolowanie i konfigurowanie
sprzętu wymagane do używania urządzeń zgodnie z żądaniami agencji
regulujących. Obejmuje to kontrolę, których kanałów można używać do
aktywnego i pasywnego skanowania oraz transmisji, kontrolę poziomu
sygnału transmisji oraz obsługę IEEE 802.11h (DFS i TPC).

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_sysconfdir}/rc.d/init.d}

%ifarch %{ix86}
install x86/%{name} $RPM_BUILD_ROOT/sbin
%endif
%ifarch %{x8664}
install x86_64/%{name} $RPM_BUILD_ROOT/sbin
%endif

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/ipw3945d ]; then
	echo "Run \"/sbin/service ipw3945d restart\" to restart ipw3945d." >&2
else
	echo "Run \"/sbin/service ipw3945d start\" to start ipw3945d." >&2
fi

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc LICENSE.ipw3945d README.ipw3945d
%attr(755,root,root) /sbin/ipw3945d
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
