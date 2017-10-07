package docker

import (
	"context"
	"fmt"
	"io"
	"os"

	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
)

func testDocker() {
	cli, err := client.NewEnvClient()
	if err != nil {
		panic(err)
	}

	ctx := context.Background()

	// list images
	images, err := cli.ImageList(ctx, types.ImageListOptions{})
	if err != nil {
		panic(err)
	}

	for _, image := range images {
		fmt.Printf("imageID: %s ; tags: %v \n", image.ID, image.RepoTags)
	}

	// crate a container
	fmt.Println("creating container")
	config := &container.Config{
		Image: "busybox",
		Cmd:   []string{"sleep", "3"},
	}
	resp, err := cli.ContainerCreate(ctx, config, nil, nil, "")
	if err != nil {
		panic(err)
	}
	out, err := cli.ContainerLogs(ctx, resp.ID, types.ContainerLogsOptions{ShowStdout: true})
	if err != nil {
		panic(err)
	}
	io.Copy(os.Stdout, out)
	fmt.Println("fnish creating container")

	// list container
	fmt.Println("listing container")
	containers, err := cli.ContainerList(ctx, types.ContainerListOptions{All: true})
	if err != nil {
		panic(err)
	}
	for _, container := range containers {
		fmt.Printf("%s %s %s %s\n", container.ID[:10], container.Image, container.Status, container.State)
	}
	fmt.Println("finish listing container")

	// run a container
	if err := cli.ContainerStart(ctx, resp.ID, types.ContainerStartOptions{}); err != nil {
		panic(err)
	}

	// list container
	fmt.Println("list container after creating")
	containers, err = cli.ContainerList(ctx, types.ContainerListOptions{All: true})
	if err != nil {
		panic(err)
	}
	for _, container := range containers {
		fmt.Printf("%s %s %s %s\n", container.ID[:10], container.Image, container.Status, container.State)
	}

	// wait
	okBodyChan, errChan := cli.ContainerWait(ctx, resp.ID, container.WaitConditionNextExit)
	if errChan == nil {
		panic("errChan is nil")
	}
	body := <-okBodyChan
	fmt.Printf("body code: %d \n", body.StatusCode)
	// err = <-errChan
	// if err != nil {
	// 	fmt.Println(err)
	// }

	// list container
	fmt.Println("list container after waiting")
	containers, err = cli.ContainerList(ctx, types.ContainerListOptions{All: true})
	if err != nil {
		panic(err)
	}
	for _, container := range containers {
		fmt.Printf("%s %s %s %s\n", container.ID[:10], container.Image, container.Status, container.State)
	}

}
