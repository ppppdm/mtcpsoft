// net.cpp
// auther : ppppdm

#include <stdio.h>
#include <stdlib.h>
#include <WinSock2.h>
#include "net.h"

#pragma comment(lib, "Ws2_32.lib")
#pragma comment(lib, "Kernel32.lib")

// Function Define
int LoadSocketLib(void);
int createThreadHandleIOCP(HANDLE ioCompletePort);
int createServerSocketAndWorkWithIOCP(HANDLE ioCompletePort);
DWORD WINAPI ServerWorkThread(LPVOID IpParam);

// Global Value
int g_totalWorkingThreads = 0;
int DefaultPort = 6000;

//The enter of server net work
void startNetWork(void)
{
	int err;

	// 加载socket动态链接库
	err = LoadSocketLib();
	if (err != 0){
		fprintf(stderr, "Can't load socket dll, will exit!\n");
		system("pause");
		exit(-1);
	}

	// 创建完成端口IOCP
	HANDLE completionPort = CreateIoCompletionPort(INVALID_HANDLE_VALUE,NULL,0,0);
	if(completionPort == NULL)
	{
		fprintf(stderr, "CreateIoCompletionPort failed. Error:%d\n", GetLastError());
		system("pause");
		exit(-1);
	}

	// 创建新线程处理IOCP队列
	err = createThreadHandleIOCP(completionPort);
	if (err != 0){
		fprintf(stderr, "Create threads for handle IOCP error！\n");
		system("pause");
		exit(-1);
	}


	// 创建服务套接字，并将请求的套接字与完成端口IOCP关联
	err = createServerSocketAndWorkWithIOCP(completionPort);
	if (err != 0){
		fprintf(stderr, "ServerSocket work error, will exit!\n");
		system("pause");
		exit(-1);
	}

	// 销毁客户端套接字和服务套接字

	// 销毁IOCP线程

	// 销毁完成端口IOCP
	
	exit_pefect:

	return;
}

// 加载socket动态链接库
int LoadSocketLib(void)
{
	WORD wVersionRequested = MAKEWORD(2, 2); // 请求2.2版本的WinSock库
	WSADATA wsaData;	// 接收Windows Socket的结构信息
	DWORD err = WSAStartup(wVersionRequested, &wsaData);

	if (0 != err){	// 检查套接字库是否申请成功
		fprintf(stderr,"Request Windows Socket Library Error!\n");
		system("pause");
		return -1;
	}
	if(LOBYTE(wsaData.wVersion) != 2 || HIBYTE(wsaData.wVersion) != 2){// 检查是否申请了所需版本的套接字库
		WSACleanup();
		fprintf(stderr,"Request Windows Socket Version 2.2 Error!\n");
		system("pause");
		return -1;
	}

	return 0;
}

// 创建新线程处理IOCP队列
int createThreadHandleIOCP(HANDLE ioCompletePort)
{
	// 确定处理器的核心数量
	SYSTEM_INFO mySysInfo;
	GetSystemInfo(&mySysInfo);
	printf("Number of Process : %d\n", mySysInfo.dwNumberOfProcessors);

	// 基于处理器的核心数量创建线程
	for(DWORD i = 0; i < (mySysInfo.dwNumberOfProcessors * 2); i++){
		// 创建服务器工作器线程，并将完成端口传递到该线程
		HANDLE ThreadHandle = CreateThread(NULL, 0, ServerWorkThread, ioCompletePort, 0, NULL);
		if(NULL == ThreadHandle){
			fprintf(stderr, "Create Thread Handle failed. Error:%d\n",GetLastError());
		}
		else {
			g_totalWorkingThreads += 1;
		}
		// 如果不再调用次工作线程，则在这里关闭其句柄
		// 考虑到服务器关闭时要确保这些线程的关闭，因此需要将这些句柄保留？
		CloseHandle(ThreadHandle);
	}

	if (g_totalWorkingThreads == 0){
		fprintf(stderr, "No work thread be created!\n");
		return -1;
	}
	return 0;
}

//
int createServerSocketAndWorkWithIOCP(HANDLE ioCompletePort)
{
	// 建立流式套接字
	SOCKET srvSocket = socket(AF_INET, SOCK_STREAM, 0);

	// 绑定SOCKET到本机
	SOCKADDR_IN srvAddr;
	srvAddr.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
	srvAddr.sin_family = AF_INET;
	srvAddr.sin_port = htons(DefaultPort);
	int bindResult = bind(srvSocket, (SOCKADDR*)&srvAddr, sizeof(SOCKADDR));
	if(SOCKET_ERROR == bindResult){
		fprintf(stderr, "Bind failed. Error:%d\n",GetLastError());
		system("pause");
		return -1;
	}

	return 0;
}