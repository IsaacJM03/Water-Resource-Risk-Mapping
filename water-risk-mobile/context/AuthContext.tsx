import React, { createContext, useState, ReactNode, useContext } from 'react';

type Role = "viewer" | "admin" | "analyst";

type AuthState = {
  role: Role;
  isAuthenticated: boolean;
  login: (role?: Role) => void;
  logout: () => void;
};
interface AuthContextType {
  role: Role;
  isAuthenticated: boolean;
  login: () => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [role, setRole] = useState<Role>("viewer");

  const login = (userRole: Role = "admin") => {
    setIsAuthenticated(true);
    setRole(userRole);
  };

  const logout = () => {
    setIsAuthenticated(false);
    setRole("viewer");
  };

  return (
    <AuthContext.Provider value={{ role, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}