import { Controller, All, Req, Res } from '@nestjs/common';
import { Request, Response } from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';

const targets = {
  '/auth': 'http://auth-service:3001',
  '/models': 'http://model-management-service:8002',
  '/enqueue': 'http://task-queue-service:8003',
  '/vectors': 'http://vector-memory-service:8004',
  '/agents': 'http://agent-service:8005',
  '/ingest': 'http://data-ingestion-service:8006',
};

@Controller()
export class ProxyController {
  @All('*')
  async proxy(@Req() req: Request, @Res() res: Response) {
    const path = req.path.split('/')[1];
    const target = targets[`/${path}`];
    if (!target) return res.status(404).send('Unknown service');

    const proxy = createProxyMiddleware({
      target,
      changeOrigin: true,
      pathRewrite: { [`^/${path}`]: '' },
    });
    proxy(req, res, () => null);
  }
}