#TODO
# - rc.init script
# - description, summary
# - exclude arch
#
%define		modname		ipw3945

Summary:	The regulatory daemon for controlling and configuring ipw3945 cards.
Name:		ipw3945d
Version:	1.7.22
Release:	0.1
License:	Intel Limited patents license
Group:		Applications/demon
Source0:	http://bughost.org/%{modname}/daemon/%{name}-%{version}.tgz
# Source0-md5:	097888f5be05eb2b9b87dcdbeeb948ce
#Source1:	%{name}-rc.init
URL:		http://ipw3945.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	%{modname}
BuildArch:	noarch
#ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The regulatory daemon is responsible for controlling and configuring
aspects of the hardware required to operate the device within
compliance of various regulatory agencies.  This includes controlling
which channels are allowed to do active/passive scanning, transmit
power levels, which channels are allowed to be transmitted on, and 
support for IEEE 802.11h (DFS and TPC).

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/rc.d/init.d}

install x86/%{name} $RPM_BUILD_ROOT%{_bindir}
#install x86_64/%{name} $RPM_BUILD_ROOT%{_bindir}
#install $SOURCE1	 $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%postun

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
%doc LICENSE.ipw3945d  README.ipw3945d
%attr(755,root,root) %{_bindir}/*
#%%attr(754,root,root) /etc/rc.d/init.d/%{name}
#%%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
