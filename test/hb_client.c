#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <pthread.h>

void *thread1()
{
    
    printf("This is sub thread\n");
	int sockfd;
	char buffer[1024], sendline[1024];
	struct sockaddr_in server_addr;
	struct hostent *host;
	int portnumber,nbytes;

    char strhost[] = "10.20.1.128";
	char port[] = "4040";
	char *sendptr = &(sendline[0]);
	char *s = "08002812d137A201307011021133151.7725,11710.4389,25.23en0192.168.001.010192.168.001.1000544061770";
	sendptr[0] = 0xaa;
	sendptr[1] = 0x55;
	sendptr+=2;
	memcpy(sendptr,s,strlen(s));
	sendptr+=strlen(s);
	sendptr[0] = 0xee;
	sendptr[1] = 0x55;
	sendptr[2] = 0x00;
	printf("%s\n",sendline);

	if((host=gethostbyname(strhost))==NULL)
	{
		fprintf(stderr,"Gethostname error\n");
		return;
	}

	if((portnumber=atoi(port))<0)
	{
		fprintf(stderr,"Usage: hostname portnumber\n");
		return;
	}

	/* 客户程序开始建立 sockfd描述符  */
	if((sockfd=socket(AF_INET,SOCK_STREAM,0))==-1)
	{
		fprintf(stderr,"Socket Error:%s\n",strerror(errno));
		return;
	}

	/* 客户程序填充服务端的资料       */
	bzero(&server_addr,sizeof(server_addr));
	server_addr.sin_family=AF_INET;
	server_addr.sin_port=htons(portnumber);
	server_addr.sin_addr=*((struct in_addr *)host->h_addr);
	/* 客户程序发起连接请求         */ 
	if(connect(sockfd,(struct sockaddr *)(&server_addr),sizeof(struct sockaddr))==-1)
	{
		fprintf(stderr,"Connect Error:%s\n",strerror(errno));
		return;
	}
	sleep(1);
	int i;
	for (i = 0; i < 10000; i++){
		/* 连接成功了           */
		if(send(sockfd,sendline,strlen(sendline),0)<0)
		{
			printf("Write Error:%s\n", strerror(errno));
			return;
		} else {
			printf("write done\n");
		}

		if((nbytes=read(sockfd,buffer,1024))==-1)
		{
			fprintf(stderr,"Read Error:%s\n",strerror(errno));
			return;
		}
		buffer[nbytes]='\0';
		printf("I have received:%s\n",buffer);
		/* 结束通讯     */
		sleep(5);
	}
	close(sockfd);
}

int main(int argc, char *argv[])
{
	pthread_t tid;

	int i;
	int total;
	int err; 
	if ( argc > 1){
		if ((total = atoi(argv[1])) < 0){
			total = 100;
		}
	}
    printf("total is %d\n",total);

    /*
	for (i=0; i < total; i++){
		if((err = pthread_create(&tid,NULL,thread1,NULL)) != 0){
			printf("create thread failed!\n");
		}
		else{
			printf("create thread success!\n");
		}
	}
    */

    
    for ( i = 0; i < total; i++){
        pid_t pid = fork();
        if (pid < 0){
        printf("error\n");
        }
    
        if (pid == 0){
            thread1();
            break;
        } else {
            printf("this is parent process\n");
        }
        sleep(1);
    }
    
	return 0;
}
