import { sha512 } from 'js-sha512'

export const hash = (password: string) => {
  return sha512(password)
}
