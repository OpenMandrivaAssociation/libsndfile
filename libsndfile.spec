%define	name	libsndfile
%define version 1.0.17
%define release %mkrel 5
%define	major	1
%define	libname	%mklibname sndfile %major

Summary:	A library to handle various audio file formats
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		Sound
Source0:	http://www.mega-nerd.com/libsndfile/%{name}-%{version}.tar.bz2
Patch: libsndfile-1.0.17+flac-1.1.3.patch
URL:		http://www.mega-nerd.com/libsndfile/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libflac-devel libogg-devel
BuildRequires: sqlite3-devel

%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

%package -n	%libname
Summary:	Shared library of sndfile
Group:		System/Libraries

%description -n	%libname
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

This package contains the shared library to run applications based on
libsndfile.

%package -n	%libname-devel 
Summary:	Libraries, includes, etc to develop libsndfile applications 
Group:		Development/C
Requires:	%libname = %version
Provides:	%name-devel = %version-%release

%description -n	%libname-devel
Libraries, include files, etc you can use to develop libsndfile applications.

%package -n	%libname-static-devel 
Summary:	Static Library for developing libsndfile applications
Group:		Development/C
Requires:	%libname-devel = %version
Provides:	%name-static-devel = %version-%release

%description -n	%libname-static-devel
This contains the static library of libsndfile needed for building apps that
link statically to libsndfile.

%package	progs
Summary:	Example progs based on libsndfile
Group:		Sound 

%description	progs
This contains sndfile-info for printing information about a sound
file and sndfile-play for playing a sound file.

%prep
%setup -q
%patch -p1
aclocal-1.9
autoconf
automake-1.9

%build
%configure2_5x
%make

%install
rm -rf %buildroot installed-docs/
%makeinstall_std transform=""
mv %buildroot%_datadir/doc/libsndfile*dev/* installed-docs

%clean
rm -rf %buildroot

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -n %libname
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO
%{_libdir}/libsndfile.so.%{major}*

%files -n %libname-devel
%defattr(-,root,root)
%doc installed-docs/*
%attr(644,root,root) %{_libdir}/libsndfile.la
%{_libdir}/libsndfile.so
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_libdir}/pkgconfig/sndfile.pc

%files -n %libname-static-devel
%defattr(-,root,root)
%{_libdir}/libsndfile.a

%files progs
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/octave/


