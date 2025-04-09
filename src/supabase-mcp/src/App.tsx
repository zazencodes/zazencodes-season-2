import { ChakraProvider, Container, VStack, Button, Flex, Heading } from '@chakra-ui/react';
import TodoList from './components/TodoList';
import AddTodo from './components/AddTodo';
import Auth from './components/Auth';
import { AuthProvider, useAuth } from './lib/AuthContext';

function TodoApp() {
  const { user, loading, signOut } = useAuth();

  if (loading) {
    return null;
  }

  if (!user) {
    return <Auth />;
  }

  return (
    <Container maxW="container.md" py={10}>
      <VStack spacing={6}>
        <Flex width="100%" justify="space-between" align="center">
          <Heading size="md">Welcome, {user.email}</Heading>
          <Button onClick={signOut} variant="ghost" size="sm">
            Sign Out
          </Button>
        </Flex>
        <AddTodo />
        <TodoList />
      </VStack>
    </Container>
  );
}

function App() {
  return (
    <ChakraProvider>
      <AuthProvider>
        <TodoApp />
      </AuthProvider>
    </ChakraProvider>
  );
}

export default App; 