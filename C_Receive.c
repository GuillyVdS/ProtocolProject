/*
    -Create an application in C, that will forever run.
    -This application should be able to receive messages from the COM/Serial/virtualSOCAT port,
    print it to the command line, then return back to waiting for information to come across the port.
    -This can be tested using "echo"
*/

#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <fcntl.h> // Contains file controls like O_RDWR
#include <errno.h> // Error integer and strerror() function
#include <unistd.h> // write(), read(), close()

#define BUFFERSIZE 512
#define SOCKET_PORT "port-one"

void ListenForMessage( int fileDescriptor, char * buffer ){
  read( fileDescriptor, buffer, BUFFERSIZE );
  buffer[strcspn( buffer, "\n" )] = 0;
  printf( "Incoming:  %s\n", buffer );
  fflush( stdout );  
  memset( buffer, 0, BUFFERSIZE );
}

int main(){
    char CharBuffer[BUFFERSIZE] = {0}; 
    int FileToRead = open( SOCKET_PORT, O_RDONLY );
    while ( true ){ 
      ListenForMessage(FileToRead, CharBuffer);      
    }
}
