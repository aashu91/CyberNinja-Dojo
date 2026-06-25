//! Integration tests for protocol message validation.

use tent_backend::protocol::validate::{
    validate_email, validate_hex_string, validate_phone, validate_symbol,
    validate_timestamp, validate_uuid, ValidationResult,
};

#[test]
fn test_validation_result_valid() {
    let result = ValidationResult::valid();
    assert!(result.valid);
    assert!(!result.has_errors());
}

#[test]
fn test_validation_result_error() {
    let result = ValidationResult::error("field1", "E001", "something broke");
    assert!(!result.valid);
    assert!(result.has_errors());
    assert_eq!(result.errors[0].field, "field1");
}

#[test]
fn test_validation_result_combine() {
    let mut r1 = ValidationResult::valid();
    let r2 = ValidationResult::error("f2", "E002", "another");
    r1.combine(r2);
    assert!(!r1.valid);
    assert_eq!(r1.errors.len(), 1);
}

#[test]
fn test_validate_email() {
    assert!(validate_email("user@example.com"));
    assert!(!validate_email("not-an-email"));
    assert!(!validate_email(""));
}

#[test]
fn test_validate_uuid() {
    assert!(validate_uuid("550e8400-e29b-41d4-a716-446655440000"));
    assert!(!validate_uuid("not-a-uuid"));
    assert!(!validate_uuid(""));
}

#[test]
fn test_validate_timestamp() {
    assert!(validate_timestamp(1700000000));
    assert!(!validate_timestamp(-1));
    assert!(!validate_timestamp(0));
}

#[test]
fn test_validate_hex_string() {
    assert!(validate_hex_string("deadbeef", 4));
    assert!(!validate_hex_string("xyz", 4));
}
