// Example of using Jobs
package main

import (
	"encoding/json"
	"fmt"

	"main/pb"
)

func main() {
	j1 := &pb.Job{
		User:       "Saitama",
		Count:      1,
		Properties: make(map[string]*pb.Value),
	}

	/* Old way before we added SetProperty method

	j1.Properties["retries"] = &pb.Value{
		Value: &pb.Value_Int{Int: 3},
	}
	j1.Properties["target"] = &pb.Value{
		Value: &pb.Value_Str{Str: "Metal Knight"},
	}
	*/

	j1.SetProperty("retries", 3)
	j1.SetProperty("target", "Metal Knight")

	fmt.Println("[j1] ", j1)

	data, err := json.Marshal(j1)
	if err != nil {
		panic(err)
	}

	fmt.Println("[json] ", string(data))

	j2 := &pb.Job{}
	if err := json.Unmarshal(data, j2); err != nil {
		panic(err)
	}
	fmt.Println("[j2] ", j2)
}
