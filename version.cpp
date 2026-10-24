#include <windows.h>

HMODULE hRealDll = nullptr;

void LoadRealVersion() {
    if (!hRealDll) {
        hRealDll = LoadLibraryW(L"versionHooked.dll");
        
        if (!hRealDll) {
            wchar_t systemPath[MAX_PATH];
            GetSystemDirectoryW(systemPath, MAX_PATH);
            wcscat_s(systemPath, MAX_PATH, L"\\version.dll");
            hRealDll = LoadLibraryW(systemPath);
        }
    }
}

extern "C" __declspec(dllexport) BOOL WINAPI GetFileVersionInfoA(LPCSTR a, DWORD b, DWORD c, LPVOID d) {
    if (!OpenMutexW(SYNCHRONIZE, FALSE, L"GTASA_Launcher_Mutex")) { ExitProcess(0); }
    LoadRealVersion();
    typedef BOOL (WINAPI *pFn)(LPCSTR, DWORD, DWORD, LPVOID);
    pFn fn = (pFn)GetProcAddress(hRealDll, "GetFileVersionInfoA");
    return fn ? fn(a, b, c, d) : FALSE;
}

extern "C" __declspec(dllexport) BOOL WINAPI GetFileVersionInfoW(LPCWSTR a, DWORD b, DWORD c, LPVOID d) {
    if (!OpenMutexW(SYNCHRONIZE, FALSE, L"GTASA_Launcher_Mutex")) { ExitProcess(0); }
    LoadRealVersion();
    typedef BOOL (WINAPI *pFn)(LPCWSTR, DWORD, DWORD, LPVOID);
    pFn fn = (pFn)GetProcAddress(hRealDll, "GetFileVersionInfoW");
    return fn ? fn(a, b, c, d) : FALSE;
}

extern "C" __declspec(dllexport) DWORD WINAPI GetFileVersionInfoSizeA(LPCSTR a, LPDWORD b) {
    if (!OpenMutexW(SYNCHRONIZE, FALSE, L"GTASA_Launcher_Mutex")) { ExitProcess(0); }
    LoadRealVersion();
    typedef DWORD (WINAPI *pFn)(LPCSTR, LPDWORD);
    pFn fn = (pFn)GetProcAddress(hRealDll, "GetFileVersionInfoSizeA");
    return fn ? fn(a, b) : 0;
}

extern "C" __declspec(dllexport) DWORD WINAPI GetFileVersionInfoSizeW(LPCWSTR a, LPDWORD b) {
    if (!OpenMutexW(SYNCHRONIZE, FALSE, L"GTASA_Launcher_Mutex")) { ExitProcess(0); }
    LoadRealVersion();
    typedef DWORD (WINAPI *pFn)(LPCWSTR, LPDWORD);
    pFn fn = (pFn)GetProcAddress(hRealDll, "GetFileVersionInfoSizeW");
    return fn ? fn(a, b) : 0;
}

extern "C" __declspec(dllexport) BOOL WINAPI VerQueryValueA(LPCVOID a, LPCSTR b, LPVOID* c, PUINT d) {
    if (!OpenMutexW(SYNCHRONIZE, FALSE, L"GTASA_Launcher_Mutex")) { ExitProcess(0); }
    LoadRealVersion();
    typedef BOOL (WINAPI *pFn)(LPCVOID, LPCSTR, LPVOID*, PUINT);
    pFn fn = (pFn)GetProcAddress(hRealDll, "VerQueryValueA");
    return fn ? fn(a, b, c, d) : FALSE;
}

extern "C" __declspec(dllexport) BOOL WINAPI VerQueryValueW(LPCVOID a, LPCWSTR b, LPVOID* c, PUINT d) {
    if (!OpenMutexW(SYNCHRONIZE, FALSE, L"GTASA_Launcher_Mutex")) { ExitProcess(0); }
    LoadRealVersion();
    typedef BOOL (WINAPI *pFn)(LPCVOID, LPCWSTR, LPVOID*, PUINT);
    pFn fn = (pFn)GetProcAddress(hRealDll, "VerQueryValueW");
    return fn ? fn(a, b, c, d) : FALSE;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    return TRUE;
}
