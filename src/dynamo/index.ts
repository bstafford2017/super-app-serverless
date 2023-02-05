import { DynamoDB } from 'aws-sdk'
import { v4 } from 'uuid'
import { hash } from '../hash'
import { User } from '../types'
import { log } from '../logging'

const TABLE_NAME = 'super-app-user-table'

const dynamo = new DynamoDB.DocumentClient({
  region: 'us-east-1'
})

export const lookupUser = async (
  userId: string,
  password: string
): Promise<User | void> => {
  log(`Looking up user for userId=${userId}`)
  const params = {
    TableName: TABLE_NAME,
    ExpressionAttributeValues: {
      ':u': userId,
      ':p': hash(password)
    },
    KeyConditionExpression: 'userId = :u and password = :p',
    Limit: 1
  }
  try {
    const { Items = [] } = await dynamo.query(params).promise()
    log(`Found user for userId=${userId}`)
    return Items.find((i) => i) as User
  } catch (e: unknown) {
    log(`Error looking up user for userId=${userId}`)
  }
}

export const insertUser = async (
  userId: string,
  password: string,
  email: string
): Promise<User | void> => {
  log(`Inserting user for userId=${userId}`)
  const id = v4()
  const datetime = new Date().toISOString()
  const params = {
    TableName: TABLE_NAME,
    Item: {
      id,
      userId: userId,
      password: hash(password),
      datetime,
      email
    }
  }
  try {
    await dynamo.put(params).promise()
    log(`Inserted user for userId=${userId}`)
    return { id, userId, password, email, datetime }
  } catch (e: unknown) {
    log(`Error inserting user for userId=${userId}`)
  }
}
