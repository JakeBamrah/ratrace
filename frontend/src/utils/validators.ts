export type validationError = { [key: string]: string | null }

export const validateYupValues = <T>(values: T | { [key: string]: number | string}, form_schema: any) => {
  // validates a yup object, expects values and schema to have same key names
  let errors = {}
  let has_errors = false
  Object.keys(values).forEach(k => {
    try {
      form_schema[k].validateSync(values[k])
    } catch (err) {
      has_errors = true
      errors[k] = err.message
    }
  })
  return { has_errors, errors }
}

export const castYupValues = <T>(values: T | { [key: string]: number | string}, form_schema: any) => {
  // validates a yup object, expects values and schema to have same key names
  let cast_values = {}
  Object.keys(values).forEach(k =>
    cast_values[k] = form_schema[k].cast(values[k])
  )
  return cast_values
}
