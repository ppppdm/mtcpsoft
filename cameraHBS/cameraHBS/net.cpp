// net.cpp
// auther : ppppdm

#include <stdio.h>
#include <stdlib.h>
#include <WinSock2.h>
#include "net.h"

#pragma comment(lib, "Ws2_32.lib")
#pragma comment(lib, "Kernel32.lib")

/**
 * 枚举变量：OPERATOIN
 * 功能：指明IO操作类型
 **/
enum OPERATOIN{
	RECV_POSTED,
	SEND_POSTED
};

/**
 * 结构体名称：PER_IO_DATA
 * 结构体功能：重叠I/O需要用到的结构体，临时记录IO数据
 **/
const int DataBuffSize  = 1024; //* 2
typedef struct
{
	OVERLAPPED overlapped;
	WSABUF databuff;
	char buffer[ DataBuffSize ];
	int BufferLen;
	int operationType;
}PER_IO_OPERATEION_DATA, *LPPER_IO_OPERATION_DATA, *LPPER_IO_DATA, PER_IO_DATA;

/**
 * 结构体名称：PER_HANDLE_DATA
 * 结构体存储：记录单个套接字的数据，包括了套接字的变量及套接字的对应的客户端的地址。
 * 结构体作用：当服务器连接上客户端时，信息存储到该结构体中，知道客户端的地址以便于回访。
 **/
typedef struct
{
	SOCKET socket;
}PER_HANDLE_DATA, *LPPER_HANDLE_DATA;


// 函数定义
int LoadSocketLib(void);
int createThreadHandleIOCP(HANDLE ioCompletePort);
int createServerSocketAndWorkWithIOCP(HANDLE ioCompletePort);
DWORD WINAPI ServerWorkThread(LPVOID IpParam);

// 全局变量
int g_totalWorkingThreads = 0;
int DefaultPort = 6000;
HANDLE hMutex = CreateMutex(NULL, FALSE, NULL);


// The enter of server net work
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
	
	//exit_pefect:

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
int createThreadHandleIOCP(HANDLE ioCompletionPort)
{
	// 确定处理器的核心数量
	SYSTEM_INFO mySysInfo;
	GetSystemInfo(&mySysInfo);
	printf("Number of Process : %d\n", mySysInfo.dwNumberOfProcessors);

	// 基于处理器的核心数量创建线程
	for(DWORD i = 0; i < (mySysInfo.dwNumberOfProcessors * 2); i++){
		// 创建服务器工作器线程，并将完成端口传递到该线程
		HANDLE ThreadHandle = CreateThread(NULL, 0, ServerWorkThread, ioCompletionPort, 0, NULL);
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
int createServerSocketAndWorkWithIOCP(HANDLE ioCompletionPort)
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

	// 将SOCKET设置为监听模式
	int listenResult = listen(srvSocket, 10);
	if(SOCKET_ERROR == listenResult){
		fprintf(stderr, "Listen failed. Error:%d\n",GetLastError());
		system("pause");
		return -1;
	}

	fprintf(stdout,"Server start, wait for client connect\n");
	while(true){
		PER_HANDLE_DATA * PerHandleData = NULL;
		SOCKADDR_IN saRemote;
		int RemoteLen;
		SOCKET acceptSocket;

		// 接收连接，并分配完成端，这儿可以用AcceptEx()
		RemoteLen = sizeof(saRemote);
		acceptSocket = accept(srvSocket, (SOCKADDR*)&saRemote, &RemoteLen);
		if(SOCKET_ERROR == acceptSocket){	// 接收客户端失败
			fprintf(stderr, "Accept Socket Error: %d\n",GetLastError());
			continue;
		}

		// 创建用来和套接字关联的单句柄数据信息结构
		PerHandleData = (LPPER_HANDLE_DATA)GlobalAlloc(GPTR, sizeof(PER_HANDLE_DATA));	// 在堆中为这个PerHandleData申请指定大小的内存
		PerHandleData -> socket = acceptSocket;

		// 将接受套接字和完成端口关联
		CreateIoCompletionPort((HANDLE)(PerHandleData -> socket), ioCompletionPort, (DWORD)PerHandleData, 0);

		// 开始在接受套接字上处理I/O使用重叠I/O机制
		// 在新建的套接字上投递一个或多个异步
		// WSARecv或WSASend请求，这些I/O请求完成后，工作者线程会为I/O请求提供服务	
		LPPER_IO_OPERATION_DATA PerIoData = NULL;
		PerIoData = (LPPER_IO_OPERATION_DATA)GlobalAlloc(GPTR, sizeof(PER_IO_OPERATEION_DATA));
		ZeroMemory(&(PerIoData -> overlapped), sizeof(OVERLAPPED));
		PerIoData->databuff.len = 1024;
		PerIoData->databuff.buf = PerIoData->buffer;
		PerIoData->operationType = RECV_POSTED;

		DWORD RecvBytes;
		DWORD Flags = 0;
		WSARecv(PerHandleData->socket, &(PerIoData->databuff), 1, &RecvBytes, &Flags, &(PerIoData->overlapped), NULL);
	}

	return 0;
}

// 服务工作线程函数
DWORD WINAPI ServerWorkThread(LPVOID IpParam)
{
	HANDLE CompletionPort = (HANDLE)IpParam;
	DWORD BytesTransferred;
	LPOVERLAPPED IpOverlapped;
	LPPER_HANDLE_DATA PerHandleData = NULL;
	LPPER_IO_DATA PerIoData = NULL;
	BOOL bRet = false;
	DWORD RecvBytes;
	DWORD Flags = 0;

	while(true){
		bRet = GetQueuedCompletionStatus(CompletionPort, &BytesTransferred, (PULONG_PTR)&PerHandleData, (LPOVERLAPPED*)&IpOverlapped, INFINITE);

		// 
		if(bRet == false){
			fprintf(stderr, "GetQueuedCompletionStatus Error:%d\n",GetLastError());
			fprintf(stderr, "BytesTransferred %d, &IpOverlapped %d\n", BytesTransferred, &IpOverlapped);
			if (IpOverlapped == NULL){
				fprintf(stderr, "WorkThread %d, will quit!\n", 1);
				break;
			}
			else {
				continue;
			}
		}
		
		PerIoData = (LPPER_IO_DATA)CONTAINING_RECORD(IpOverlapped, PER_IO_DATA, overlapped);

		// 检查在套接字上是否有错误发生
		if(0 == BytesTransferred){
			fprintf(stdout, "operationType %d\n", PerIoData->operationType);
			fprintf(stdout, "client close! Thread %d\n", GetCurrentThreadId());
			closesocket(PerHandleData->socket);
			GlobalFree(PerHandleData);
			GlobalFree(PerIoData);		
			continue;
		}

		// 操作完成没有发生错误
		if(PerIoData->operationType == RECV_POSTED){
			WaitForSingleObject(hMutex,INFINITE);
			fprintf(stdout, "A Client says: %s\n", PerIoData->databuff.buf);
			ReleaseMutex(hMutex);

			// 为下一个重叠调用建立单I/O操作数据
			ZeroMemory(&(PerIoData->overlapped), sizeof(OVERLAPPED)); // 清空内存
			PerIoData->databuff.len = 1024;
			//ZeroMemory(&(PerIoData->buffer), 1024); // 清空内存
			//PerIoData->databuff.buf = PerIoData->buffer;
			//PerIoData->operationType = SEND_POSTED;
			WSASend(PerHandleData->socket, &(PerIoData->databuff), 1, NULL, Flags, &(PerIoData->overlapped), NULL);
		}
		if(PerIoData->operationType == SEND_POSTED){
			WaitForSingleObject(hMutex,INFINITE);
			fprintf(stdout, "Operate type send_posted, thread %d, bytes trans %d\n", GetCurrentThreadId(),BytesTransferred);
			ReleaseMutex(hMutex);

			// 为下一个重叠调用建立单I/O操作数据
			ZeroMemory(&(PerIoData->overlapped), sizeof(OVERLAPPED)); // 清空内存
			PerIoData->databuff.len = 1024;
			PerIoData->databuff.buf = PerIoData->buffer;
			PerIoData->operationType = RECV_POSTED;
			WSARecv(PerHandleData->socket, &(PerIoData->databuff), 1, &RecvBytes, &Flags, &(PerIoData->overlapped), NULL);
		}
	}

	return 0;
}