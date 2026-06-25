package gateway

import (
	"fmt"
	"testing"
	"time"
)

func TestWSConnectionManagerRegister(t *testing.T) {
	wm := NewWSConnectionManager(DefaultGatewayConfig())
	conn := &WSConnection{
		ID:        "conn-1",
		UserID:    "user-1",
		Connected: time.Now(),
	}
	wm.Register(conn)

	if wm.Count() != 1 {
		t.Fatalf("expected 1 connection after register, got %d", wm.Count())
	}

	got := wm.Get("conn-1")
	if got == nil || got.ID != "conn-1" {
		t.Fatal("Get should return the registered connection")
	}
}

func TestWSConnectionManagerUnregister(t *testing.T) {
	wm := NewWSConnectionManager(DefaultGatewayConfig())
	conn := &WSConnection{ID: "conn-2", UserID: "user-2", Connected: time.Now()}
	wm.Register(conn)
	wm.Unregister("conn-2")

	if wm.Count() != 0 {
		t.Fatalf("expected 0 connections after unregister, got %d", wm.Count())
	}

	got := wm.Get("conn-2")
	if got != nil {
		t.Fatal("Get should return nil after unregister")
	}
}

func TestWSConnectionManagerDrain(t *testing.T) {
	wm := NewWSConnectionManager(DefaultGatewayConfig())
	for i := 0; i < 5; i++ {
		wm.Register(&WSConnection{
			ID:        fmt.Sprintf("drain-%d", i),
			UserID:    "user-drain",
			Connected: time.Now(),
		})
	}

	if wm.Count() != 5 {
		t.Fatalf("expected 5 before drain, got %d", wm.Count())
	}

	wm.Drain()

	if wm.Count() != 0 {
		t.Fatalf("expected 0 after drain, got %d", wm.Count())
	}
}

func TestWSConnectionManagerGetNonExistent(t *testing.T) {
	wm := NewWSConnectionManager(DefaultGatewayConfig())
	got := wm.Get("does-not-exist")
	if got != nil {
		t.Fatal("Get should return nil for non-existent connection")
	}
}

func TestWSConnectionManagerRegisterMultiple(t *testing.T) {
	wm := NewWSConnectionManager(DefaultGatewayConfig())
	for i := 0; i < 10; i++ {
		wm.Register(&WSConnection{
			ID:        fmt.Sprintf("multi-%d", i),
			UserID:    fmt.Sprintf("user-%d", i),
			Connected: time.Now(),
		})
	}

	if wm.Count() != 10 {
		t.Fatalf("expected 10 connections, got %d", wm.Count())
	}
}

func TestWSConnectionManagerUnregisterNonExistent(t *testing.T) {
	wm := NewWSConnectionManager(DefaultGatewayConfig())
	// Should not panic
	wm.Unregister("ghost-connection")
	if wm.Count() != 0 {
		t.Fatal("unregister non-existent should be no-op")
	}
}
