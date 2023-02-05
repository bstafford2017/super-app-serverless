import {
  APIGatewayProxyEvent,
  Context,
  APIGatewayProxyResult
} from 'aws-lambda'
import { insertUser, lookupUser } from '../dynamo'
import jwt from 'jsonwebtoken'
import { User } from '../types'
import { log, setupLog } from '../logging'

interface LoginRequest {
  userId: string
  password: string
}

export const login = async (
  event: APIGatewayProxyEvent,
  context: Context
): Promise<APIGatewayProxyResult> => {
  setupLog(event, context)
  log('Request to /login')

  const { body = '' } = event
  const { userId = '', password = '' }: LoginRequest = JSON.parse(body || '')

  if (!userId && !password) {
    log('Invalid input')
    return {
      statusCode: 400,
      body: JSON.stringify({ message: 'Invalid input' })
    }
  }

  const user: User | void = await lookupUser(userId, password)

  if (!user) {
    log('Invalid credentials')
    return {
      statusCode: 400,
      body: JSON.stringify({ message: 'Invalid credentials' })
    }
  }

  const { id } = user

  log(`Authorized request to /login id=${id}, userId=${userId}`)
  return {
    statusCode: 200,
    body: JSON.stringify({
      token: jwt.sign({
        id
      })
    })
  }
}

export interface RegisterRequest {
  userId: string
  password: string
  confirmPassword: string
  email: string
}

export const register = async (
  event: APIGatewayProxyEvent,
  context: Context
): Promise<APIGatewayProxyResult> => {
  setupLog(event, context)
  log('Request to /register')

  const { body = '' } = event
  const {
    userId = '',
    password = '',
    confirmPassword = '',
    email = ''
  }: RegisterRequest = JSON.parse(body || '')

  if (!userId && !password && !confirmPassword && !email) {
    log('Invalid input')
    return {
      statusCode: 400,
      body: JSON.stringify({ message: 'Invalid input' })
    }
  }

  if (password !== confirmPassword) {
    log('Invalid input')
    return {
      statusCode: 400,
      body: JSON.stringify({ message: 'Invalid input' })
    }
  }

  const existingUser: User | void = await lookupUser(userId, password)

  if (existingUser) {
    log('User already exists')
    return {
      statusCode: 400,
      body: JSON.stringify({ message: 'User already exists' })
    }
  }

  const newUser: User | void = await insertUser(userId, password, email)

  if (!newUser) {
    log(`Failed to insert user for userId=${userId}`)
    return {
      statusCode: 500,
      body: JSON.stringify({ message: `Failed to register userId=${userId}` })
    }
  }

  const { id } = newUser

  log(`Sucessfully /register for id=${id} userId=${userId}`)
  return {
    statusCode: 200,
    body: JSON.stringify({
      token: jwt.sign({
        id
      })
    })
  }
}
