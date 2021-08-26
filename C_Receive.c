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
#include <stdlib.h>

#define BUFFERSIZE 512
#define SOCKET_PORT "port-one"
#define DESTINATION_FILE "inputfile.txt"

/*Takes */
void writeToFile(char * textinput){
  FILE *fileptr = fopen(DESTINATION_FILE, "a");
  printf(" %s\n", strerror(errno));
  if(fileptr == NULL)
  {
    printf("File-Error");
    exit(1);
  }
  fprintf(fileptr, "\n%s", textinput );
  fclose(fileptr);
}

/*Takes a file descriptor for a socket and reads up to the count of BUFFERSIZE,
storing this into the buffer.

*/

void ListenForMessage( int fileDescriptor, char * buffer ){
  read( fileDescriptor, buffer, BUFFERSIZE );
  buffer[strcspn( buffer, "\n" )] = 0;
  printf( "Incoming:  %s\n", buffer );
  fflush( stdout ); /* Prints what's in the buffer as the while loop sometimes 
  skips print statements. */
  writeToFile(buffer);             //Writes contents of the buffer into a file.
  memset( buffer, 0, BUFFERSIZE ); //Clears the buffer for the next operation
}

/**/

int main(){
    char CharBuffer[BUFFERSIZE] = {0};
    int FileToRead = open( SOCKET_PORT, O_RDONLY );
    while ( true ){
      ListenForMessage(FileToRead, CharBuffer);
    }
}
