
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

/*Takes a char pointer as input. The function creates a filepointer object, opens
the DESTINATION_FILE in append mode and stores this into the filepointer. The
function also checks whether a file pointer was succesfully created through use
of an if statement. fprintf will store the contents of the char pointer into the
file.*/

void writeToFile(char * textinput){
  FILE *fileptr = fopen(DESTINATION_FILE, "a");
  //printf(" %s\n", strerror(errno));
  if(fileptr == NULL)
  {
    printf("File-Error %s\n", strerror(errno));
    exit(1);
  }
  fprintf(fileptr, "\n%s", textinput );
  fclose(fileptr);
}

/*Takes a file descriptor for a socket and reads up to the count of BUFFERSIZE,
storing this into the buffer. strcspn is used to find the newline inside
the buffer and remove it. fflush is used to force the output to print as the
while loop has a tendency to block printf from working.
Finally the contents of the buffer get written into a text file and
the memset clears the buffer for the next use of this function.
*/

void ListenForMessage( int fileDescriptor, char * buffer ){
  read( fileDescriptor, buffer, BUFFERSIZE ); //
  buffer[strcspn( buffer, "\n" )] = 0;
  printf( "Incoming:  %s\n", buffer );
  fflush( stdout );
  writeToFile(buffer);
  memset( buffer, 0, BUFFERSIZE );
}


int main(){
    char CharBuffer[BUFFERSIZE] = {0};
    int FileToRead = open( SOCKET_PORT, O_RDONLY );
    if(FileToRead == NULL)
    {
      printf("Socket-Error %s\n", strerror(errno));
      exit(1);
    }
    while ( true ){
      ListenForMessage(FileToRead, CharBuffer);
    }
}
