package main

import (
	"log"
	"fmt"
	"time"
)

func main() {


	for {
		log.Println("This is a standard log to stderr.")
		fmt.Println(time.Now(), "This is a standard log to output stdout. ")
 
		time.Sleep(1 * time.Second)
	}
}