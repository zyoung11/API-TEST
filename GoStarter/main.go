package main

import (
	"fmt"
	"os"
	"os/exec"
	"sync"
	"time"
)

var (
	exePath = "./Boltbase"
	dbPath  = "./Boltbase.db"
	uv      = "uv run main.py"
)

var (
	runningProcesses = make(map[string]*exec.Cmd)
	mutex            = &sync.Mutex{}
)

func ExecuteFile(filePath string) error {
	cmd := exec.Command(filePath)
	err := cmd.Start()
	if err != nil {
		return fmt.Errorf("failed to start file: %w", err)
	}

	mutex.Lock()
	runningProcesses[filePath] = cmd
	mutex.Unlock()

	go func() {
		cmd.Wait()
		mutex.Lock()
		delete(runningProcesses, filePath)
		mutex.Unlock()
	}()

	fmt.Printf("Started process for %s with PID: %d\n", filePath, cmd.Process.Pid)
	return nil
}

func StopProcess(path string) error {
	mutex.Lock()
	defer mutex.Unlock()
	cmd, ok := runningProcesses[path]
	if !ok {
		fmt.Printf("Process not found for path: %s. It might have already terminated.\n", path)
		return nil
	}
	err := cmd.Process.Kill()
	if err != nil {
		return fmt.Errorf("failed to kill process: %w", err)
	}
	delete(runningProcesses, path)
	fmt.Printf("Killed process for %s\n", path)
	return nil
}

func ExecuteCommandSync(command string) error {
	cmd := exec.Command("sh", "-c", command)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		return fmt.Errorf("command failed: %s: %w", command, err)
	}
	return nil
}

func main() {
	if err := ExecuteFile(exePath); err != nil {
		fmt.Printf("Failed to start: %v\n", err)
		os.Exit(1)
	}

	time.Sleep(2 * time.Second)

	fmt.Println("Running test script...")
	if err := ExecuteCommandSync(uv); err != nil {
		fmt.Printf("Python script failed: %v\n", err)
	}

	if err := StopProcess(exePath); err != nil {
		fmt.Printf("Failed to stop Boltbase process: %v\n", err)
	}

	if err := os.Remove(dbPath); err != nil {
		fmt.Printf("Failed to remove Boltbase.db: %v\n", err)
	}

	fmt.Println("All done.")
}
