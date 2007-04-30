#TODO
# - rc.init script
#
Summary:	The regulatory daemon for controlling and configuring ipw3945 cards
Summary(pl.UTF-8):	Demon do kontrolowania i konfigurowania kart ipw3945
Name:		ipw3945d
Version:	1.7.22
Release:	1
License:	Intel Limited patents license
Group:		Applications/demon
Source0:	http://bughost.org/ipw3945/daemon/%{name}-%{version}.tgz
# Source0-md5:	097888f5be05eb2b9b87dcdbeeb948ce
#Source1:	%{name}-rc.init
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
install -d $RPM_BUILD_ROOT{/sbin,/etc/rc.d/init.d}

%ifarch %{ix86}
install x86/%{name} $RPM_BUILD_ROOT/sbin
%endif
%ifarch %{x8664}
install x86_64/%{name} $RPM_BUILD_ROOT/sbin
%endif

#install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun 
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc LICENSE.ipw3945d README.ipw3945d
%attr(755,root,root) /sbin/*
#%%attr(754,root,root) /etc/rc.d/init.d/%{name}
#%%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
