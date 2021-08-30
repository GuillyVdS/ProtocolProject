
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <fcntl.h> // Contains file controls like O_RDWR
#include <errno.h> // Error integer and strerror() function
#include <unistd.h> // write(), read(), close()
#include <stdlib.h>

#define BUFFERSIZE 512
#define SOCKET_PORT "port-one"
#define TEXT_FILE "inputfile.txt"

/*Takes a char pointer and destination file as input. The function creates a filepointer object, opens
the destination_file in append mode and stores this into the filepointer. The
function also checks whether a file pointer was succesfully created through use
of an if statement. fprintf will store the contents of the char pointer into the
file.*/

void writeToFile(const char * destination_file, char * textinput ){
  FILE *fileptr = fopen( destination_file, "a" );
  if( fileptr == NULL )
  {
    printf( "File-Error %s\n", strerror( errno ));
    exit( 1 );
  }
  fprintf( fileptr, "\n%s", textinput );
  fclose( fileptr );
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
  int testvar = write(fileDescriptor, buffer, strlen(buffer));
  if( testvar == -1 ){
      printf( "File-Error %s\n", strerror( errno ));
  }
  writeToFile( TEXT_FILE, buffer );
  memset( buffer, 0, BUFFERSIZE );
}


int main(){
    char CharBuffer[BUFFERSIZE] = {0};
    int FileToRead = open( SOCKET_PORT, O_RDWR );
    if( FileToRead == -1 )
    {
      printf( "Socket-Error %s\n ", strerror( errno ) );
      exit(1);
    }
    while ( true ){
      ListenForMessage( FileToRead, CharBuffer );
    }
}
