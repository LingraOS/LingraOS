import jwt from 'jsonwebtoken';

const SECRET = 'very-secret-key';

export function verifyToken(token: string) {
  return jwt.verify(token, SECRET);
}

export function signToken(payload: object) {
  return jwt.sign(payload, SECRET);
}