import NextAuth from 'next-auth';
import type { NextAuthConfig } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import { api } from './api';

export const authOptions: NextAuthConfig = {
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email', placeholder: 'your@email.com' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        try {
          const response = await api.auth.login(credentials.email as string, credentials.password as string);
          const user = response.data;
          return {
            id: user.user_id,
            email: credentials.email as string,
            name: user.name,
            apiKey: user.api_key,
            tier: user.tier,
          } as any;
        } catch (error) {
          console.error('Login failed:', error);
          return null;
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user, trigger, session }) {
      if (user) {
        token.apiKey = (user as any).apiKey;
        token.tier = (user as any).tier;
        token.id = user.id;
      }
      if (trigger === "update" && session?.user) {
        if (session.user.tier) token.tier = session.user.tier;
        if (session.user.name) token.name = session.user.name;
        if (session.user.apiKey) token.apiKey = session.user.apiKey;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        (session.user as any).apiKey = token.apiKey;
        (session.user as any).tier = token.tier;
        (session.user as any).id = token.id;
      }
      return session;
    },
  },
  pages: {
    signIn: '/login',
  },
  session: {
    strategy: 'jwt',
  },
};

export const { handlers, auth, signIn, signOut } = NextAuth(authOptions);
export default authOptions;
