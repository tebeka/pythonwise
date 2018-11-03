// Utility methods for Job to make nice API and smooth integration with JSON

package pb

import (
	"encoding/json"
	"fmt"
	"reflect"
)

// SetProperty sets a Job property
func (j *Job) SetProperty(key string, value interface{}) error {
	v, err := ValueFromGo(value)
	if err != nil {
		return err
	}

	j.Properties[key] = v
	return nil
}

// ValueFromGo returns a new *Value for a native Go value
func ValueFromGo(v interface{}) (*Value, error) {
	var iv isValue_Value

	switch v.(type) {
	case int, int8, int16, int32, int64:
		// Hack to get Int value
		iv = &Value_Int{Int: reflect.ValueOf(v).Int()}
	case string:
		iv = &Value_Str{Str: v.(string)}
	default:
		return nil, fmt.Errorf("unsupported type for Value - %T", v)
	}

	return &Value{Value: iv}, nil
}

// MarshalJSON marshal value as JSON object
// (Implement json.Marshaler interface)
func (v *Value) MarshalJSON() ([]byte, error) {
	switch v.GetValue().(type) {
	case *Value_Int:
		return json.Marshal(v.GetInt())
	case *Value_Str:
		return json.Marshal(v.GetStr())
	}

	return nil, fmt.Errorf("unknown Value type - %T", v.GetValue())
}

// UnmarshalJSON will unmarshal encoded native Go type to value
// (Implement json.Unmarshaler interface)
func (v *Value) UnmarshalJSON(data []byte) error {
	var i interface{}
	if err := json.Unmarshal(data, &i); err != nil {
		return err
	}

	switch i.(type) {
	case float64: // JSON encodes numbers as floats
		ival := int64(i.(float64))
		v.Value = &Value_Int{Int: ival}
	case string:
		v.Value = &Value_Str{Str: i.(string)}
	default:
		return fmt.Errorf("unsupported type for value - %T", i)
	}

	return nil
}
