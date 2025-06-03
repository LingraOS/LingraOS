import { Injectable, UnauthorizedException } from '@nestjs/common';
import * as bcrypt from 'bcryptjs';
import * as jwt from 'jsonwebtoken';
import { RegisterDto, LoginDto } from './dto';

const users = []; // In-memory user storage
const JWT_SECRET = 'very-secret-key';

@Injectable()
export class AuthService {
  async register(dto: RegisterDto) {
    const exists = users.find(u => u.email === dto.email);
    if (exists) throw new Error('User already exists');
    const hashed = await bcrypt.hash(dto.password, 10);
    const user = { id: users.length + 1, email: dto.email, password: hashed, role: 'user' };
    users.push(user);
    return { message: 'Registered' };
  }

  async login(dto: LoginDto) {
    const user = users.find(u => u.email === dto.email);
    if (!user || !(await bcrypt.compare(dto.password, user.password)))
      throw new UnauthorizedException('Invalid credentials');
    const token = jwt.sign({ id: user.id, email: user.email, role: user.role }, JWT_SECRET);
    return { token };
  }

  verify(token: string) {
    return jwt.verify(token, JWT_SECRET);
  }
}