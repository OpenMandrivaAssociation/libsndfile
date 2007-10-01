%define prel pre11
%define	major 1
%define	libname	%mklibname sndfile %{major}
%define develname %mklibname sndfile -d
%define staticname %mklibname sndfile -d -s

Summary:	A library to handle various audio file formats
Name:		libsndfile
Version:	1.0.18
Release:	%mkrel 0.%{prel}.7
License:	LGPL
Group:		Sound
URL:		http://www.mega-nerd.com/libsndfile/
Source0:	http://www.mega-nerd.com/libsndfile/%{name}-%{version}%{prel}.tar.bz2
<<<<<<< .mine
Patch0:		libsndfile-CVE-2007-4974.diff
=======
Patch: libsndfile-1.0.17-gentoo-CVE-2007-4974.patch
>>>>>>> .r94197
BuildRequires:	libogg-devel
BuildRequires:	sqlite3-devel
BuildRequires:	libflac-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

%package -n %{libname}
Summary:	Shared library of sndfile
Group:		System/Libraries

%description -n	%{libname}
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

This package contains the shared library to run applications based on
libsndfile.

%package -n %{develname}
Summary:	Libraries, includes, etc to develop libsndfile applications 
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	libflac-devel
Provides:	sndfile-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname sndfile 1 -d

%description -n	%{develname}
Libraries, include files, etc you can use to develop libsndfile applications.

%package -n %{staticname}
Summary:	Static Library for developing libsndfile applications
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%mklibname sndfile 1 -d -s

%description -n	%{staticname}
This contains the static library of libsndfile needed for building apps that
link statically to libsndfile.

%package progs
Summary:	Example progs based on libsndfile
Group:		Sound 

%description	progs
This contains sndfile-info for printing information about a sound
file and sndfile-play for playing a sound file.

%prep

%setup -qn %{name}-%{version}%{prel}
<<<<<<< .mine
%patch0 -p0
=======
%patch -p1
>>>>>>> .r94197

%build
%configure2_5x
%make

%install
rm -rf %{buildroot} 

%makeinstall_std 
rm -rf %{buildroot}%{_includedir}/FLAC

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO
%{_libdir}/libsndfile.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc %{_docdir}/libsndfile1-dev
%attr(644,root,root) %{_libdir}/libsndfile.la
%{_libdir}/libsndfile.so
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_libdir}/pkgconfig/sndfile.pc

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/libsndfile.a

%files progs
%defattr(-,root,root)
%{_bindir}/sndfile-*
%{_mandir}/man1/*
%{_datadir}/octave/
