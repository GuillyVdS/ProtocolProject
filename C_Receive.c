
#include <errno.h> // Error integer and strerror() function
#include <fcntl.h> // Contains file controls like O_RDWR
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> // write(), read(), close()

#define BUFFERSIZE 512
#define SOCKET_PORT "port-one"
#define TEXT_FILE "inputfile.txt"
#define STX (char)0xAA
#define ETX (char)0xAB
#define EXE (char)0xAC

/*Takes a char pointer and destination file as input. The function creates a filepointer object, opens
the destination_file in append mode and stores this into the filepointer. The
function also checks whether a file pointer was succesfully created through use
of an if statement. fprintf will store the contents of the char pointer into the
file.*/

void writeToFile(const char* destination_file, char* textinput)
{
  FILE* fileptr = fopen(destination_file, "a");
  if (fileptr == NULL) {
    printf("File-Error %s\n", strerror(errno));
    exit(1);
  }
  fprintf(fileptr, "\n%s", textinput);
  fclose(fileptr);
}

/*Function used to encode char buffer */

void Encode_Message( char * buffer, int sizeOfBuffer ,char * outsidebuffer , int outsidebufferSize)
{
  /*Create char variable to keep track of Payload_Length.*/
  char Payload_Length = (char)sizeOfBuffer;
  /*Create buffer to store encoded character*/
  //char Encoded_Message[1000] = {0};

  /*creates ptr to Encoded_Message*/
  char * ptr_Encoded_Message = outsidebuffer;


  /*creates start byte and sets a zeroed payload size byte*/
  *ptr_Encoded_Message++ = STX;
  *ptr_Encoded_Message++ = '0';


  /*while loop executes as long as index sizeOfBuffer is above 0. This will be
  decremented on each loop.*/
  while( sizeOfBuffer )
  {
    /*This if else statement checks whether the payload contains any of the
    command bytes. It handles these by inserting an exception byte in front
    of each offending byte. Each time this occurs the Payload_Length is
    incremented by one to keep track of the length of the payload.*/
    if( *buffer == STX)
    {
      *ptr_Encoded_Message = EXE;
      ptr_Encoded_Message++;
      Payload_Length++;
    }
    else if( *buffer == ETX)
    {
      *ptr_Encoded_Message = EXE;
      ptr_Encoded_Message++;
      Payload_Length++;

    }
    else if( *buffer == EXE)
    {
      *ptr_Encoded_Message = EXE;
      ptr_Encoded_Message++;
      Payload_Length++;

    }

    /*stores value from buffer at ptr for encoded message*/
    *ptr_Encoded_Message = *buffer;
    //printf("%02X ", *ptr_Encoded_Message);

    /*Increments buffer and ptr for next iteration. Decrements sizeOfBuffer*/
    buffer++;
    ptr_Encoded_Message++;
    sizeOfBuffer--;


    fflush( stdout );
  }

  /*Set end byte ETX and adjusts payload byte to correct value*/
  *ptr_Encoded_Message = ETX;
  outsidebuffer[1] = Payload_Length;
  printf("%02X", *outsidebuffer);
  //memcpy ( outsidebuffer, Encoded_Message, sizeof(Encoded_Message) );
  //printf("%02X", *Encoded_Message);
  //write( FileToRead, Encoded_Message, sizeof( Encoded_Message ) );
  //printf("Payload is %d  bytes long\n", Payload_Length );
}


void Decode_Message()
{



}

/*Takes a file descriptor for a socket and reads up to the count of BUFFERSIZE,
storing this into the buffer. strcspn is used to find the newline inside
the buffer and remove it. fflush is used to force the output to print as the
while loop has a tendency to block printf from working.
Finally the contents of the buffer get written into a text file and
the memset clears the buffer for the next use of this function.
*/

void ListenForMessage(int fileDescriptor, char* buffer)
{
  read(fileDescriptor, buffer, BUFFERSIZE); //
  buffer[strcspn(buffer, "\n")] = 0;
  printf("Incoming:  %s\n", buffer);
  fflush(stdout);
  int testvar = write(fileDescriptor, buffer, strlen(buffer));
  if (testvar == -1) {
    printf("File-Error %s\n", strerror(errno));
  }
  writeToFile(TEXT_FILE, buffer);
  memset(buffer, 0, BUFFERSIZE);
}

int main()
{
  /*char CharBuffer[BUFFERSIZE] = { 0 };
  int FileToRead = open(SOCKET_PORT, O_RDWR);
  if (FileToRead == -1) {
    printf("Socket-Error %s\n ", strerror(errno));
    exit(1);
  }
  while (true) {
    ListenForMessage(FileToRead, CharBuffer);
  }
  */
  int FileToRead = open(SOCKET_PORT, O_RDWR);
  char testmessage[100] = {0};
  char sendBuffer[100] = {0};
  strcpy( testmessage, "testvalued" );
  testmessage[4] = (char)0xAB;
  testmessage[8] = (char)0xAC;
  testmessage[6] = (char)0xAA;
  Encode_Message( testmessage, strlen( testmessage ), sendBuffer, 100 );
  write( FileToRead, sendBuffer, sizeof( sendBuffer ) );

}
