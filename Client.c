// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#define PORT 8888
#define TRUE 1 
#define FALSE 0
typedef struct {
char sub_msg[1024];
} CM_Subscribe;

int main(int argc, char const *argv[])
{
	CM_Subscribe message;
	struct sockaddr_in address;
	int sock = 0, valread;
	struct sockaddr_in serv_addr;
	char *hello = "Hello from client";
	char buffer[1024] = {0};
	if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
	{
		printf("\n Socket creation error \n");
		return -1;
	}

	memset(&serv_addr, '0', sizeof(serv_addr));

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);
	
	// Convert IPv4 and IPv6 addresses from text to binary form
	if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0) 
	{
		printf("\nInvalid address/ Address not supported \n");
		return -1;
	}

	if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
	{
		printf("\nConnection Failed \n");
		return -1;
	}
	//trying to send cm_subscribe
        printf("Player name: ");
        bzero(buffer,sizeof(buffer));
        fgets(buffer,sizeof(buffer)-1,stdin);
        printf("CM_Subscribe message will contain : <%s>\n", buffer);
	strcpy(message.sub_msg,buffer);	
	send(sock, &message, sizeof(message), 0);
	//done with CM_Subscribe
	send(sock , hello , strlen(hello) , 0 );
	printf("Hello message sent\n");
	valread = read( sock , buffer, 1024);
	printf("%s\n",buffer );
	
	while(TRUE){
		//just keep running
	}
	return 0;
}
