import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import * as jwt from 'jsonwebtoken';

@Injectable()
export class AuthMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    if (req.path.startsWith('/auth')) return next();
    const auth = req.headers.authorization;
    if (!auth || !auth.startsWith('Bearer ')) return res.status(401).send('No token');
    try {
      const token = auth.split(' ')[1];
      req['user'] = jwt.verify(token, 'very-secret-key');
      next();
    } catch {
      return res.status(401).send('Invalid token');
    }
  }
}