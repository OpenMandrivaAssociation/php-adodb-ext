%define modname adodb-ext
%define src_version 504
%define soname %{modname}.so
%define inifile A10_%{modname}.ini

%define _requires_exceptions pear(phplens/adodb/adodb.inc.php)

Summary:	ADOdb extension for PHP
Name:		php-%{modname}
Version:	5.0.4
Release:	%mkrel 26
Epoch:		1
Group:		Development/PHP
License:	BSD
URL:		https://phplens.com/
Source0:	http://phplens.com/lens/dl/%{modname}-%{src_version}.tar.bz2
Source1:	%{name}.ini
Requires:	php-adodb >= 1:4.81
Requires:	php >= 3:5.2.0
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The ADOdb PHP extension provides up to 75% speedup by replacing parts of ADOdb
with C code. This extension is compatible with ADOdb 3.32 or later.

%prep

%setup -q -n adodb-%{src_version}

cp %{SOURCE1} %{inifile}

%build
%serverbuild

phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so %{modname}.so

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS test-adodb.php README*
%config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%{_libdir}/php/extensions/%{soname}
