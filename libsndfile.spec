%define major 1
%define libname %mklibname sndfile %{major}
%define devname %mklibname sndfile -d

%bcond_with	octave
%bcond_with	bootstrap

Summary:	A library to handle various audio file formats
Name:		libsndfile
Version:	1.0.28
Release:	5
License:	LGPLv2+
Group:		Sound
Url:		http://www.mega-nerd.com/libsndfile/
Source0:	http://www.mega-nerd.com/libsndfile/files/%{name}-%{version}.tar.gz
Patch0:	libsndfile-1.0.25-system-gsm.patch
Patch1:	libsndfile-1.0.25-zerodivfix.patch
Patch2:	libsndfile-1.0.28-flacbufovfl.patch
Patch3:	libsndfile-1.0.29-cve2017_6892.patch
#libsndfile-1.0.29-cve2017_6892.patch
# from upstream, for <= 1.0.28, rhbz#1483140
Patch4:	libsndfile-1.0.28-cve2017_12562.patch
BuildRequires:	gsm-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(celt)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(vorbis)
%if !%{with bootstrap}
%ifarch %{ix86} x86_64
BuildRequires:	nasm
%endif
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(samplerate)
%endif

%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

%package -n	%{libname}
Summary:	Shared library of sndfile
Group:		System/Libraries
# (tpg) add compat provides
%if "%_lib" == "lib64"
Provides:		libsndfile.so.1(libsndfile.so.1.0)(64bit)
%else
Provides:		libsndfile.so.1(libsndfile.so.1.0)
%endif

%description -n	%{libname}
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

This package contains the shared library to run applications based on
libsndfile.

%package -n	%{devname}
Summary:	Libraries, includes, etc to develop libsndfile applications 
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	sndfile-devel = %{version}-%{release}

%description -n	%{devname}
Libraries, include files, etc you can use to develop libsndfile applications.

%package	progs
Summary:	Example progs based on libsndfile
Group:		Sound 

%description	progs
This contains sndfile-info for printing information about a sound
file and sndfile-play for playing a sound file.

%if %{with octave}
%package	octave
Summary:	Octave modules based on libsndfile
Group:		Sound 
BuildRequires:	octave-devel

%description	octave
This contains octave modules based on libsndfile for reading, writing and 
playing audio files.
%endif

%prep
%autosetup -p1

rm -r src/GSM610
autoreconf -fi -IM4

%build
%configure
%make_build

%install
%make_install 
rm -rf %{buildroot}%{_includedir}/FLAC

%files -n %{libname}
%{_libdir}/libsndfile.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README
%doc %{_docdir}/libsndfile
%doc ChangeLog
%{_libdir}/libsndfile.so
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_libdir}/pkgconfig/sndfile.pc

%files progs
%{_bindir}/sndfile-*
%{_mandir}/man1/*

%if %{with octave}
%files octave
%{_datadir}/octave/
%dir %{_libdir}/octave/*/site/oct/%{_target_platform}/sndfile
%{_libdir}/octave/*/site/oct/%{_target_platform}/sndfile/PKG_ADD
%{_libdir}/octave/*/site/oct/%{_target_platform}/sndfile/sndfile.oct
%endif
